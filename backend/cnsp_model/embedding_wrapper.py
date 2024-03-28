import pandas as pd
from scipy.spatial.distance import cdist, euclidean, squareform, pdist
import numpy as np
import ot

class EmbeddingWrapper(object):
    def __init__(self, word2VecModel):
        self.model = word2VecModel
        self.vocab_len = len(self.model.wv.index_to_key)
        self.word2index = dict(zip([self.model.wv.index_to_key[i] for i in range(self.vocab_len)],
                              [i for i in range(self.vocab_len)]))
        self.word_index_df = pd.DataFrame(data=list(self.word2index.items()), columns=['product_id', 'emb_id'])

    def lookup_ind_f(self, i):
        return self.word2index[i]

    def get_closest_of_set(self, item_id, set_of_candidates):
        vec_of_interest = self.model.wv.vectors[item_id]
        closest = np.argmin([euclidean(vec_of_interest, self.model.wv.vectors[x]) for x in set_of_candidates])
        return set_of_candidates[closest]
    
    def find_closest_from_preds(self, pred, candidates_l_l):
        closest_from_history = []
        for p in pred:
            closest_from_history.append(self.get_closest_of_set(p, [x for seq in candidates_l_l for x in seq]))
        return closest_from_history
        
    def basket_dist_REMD(self, baskets):  
        basket1_vecs = self.model.wv.vectors[[x for x in baskets[0]]]
        basket2_vecs = self.model.wv.vectors[[x for x in baskets[1]]]
        
        distance_matrix = cdist(basket1_vecs, basket2_vecs)
        
        return max(np.mean(np.min(distance_matrix, axis=0)),
                   np.mean(np.min(distance_matrix, axis=1)))
        
    def basket_dist_EMD(self, baskets):
        basket1 = baskets[0]
        basket2 = baskets[1]
        dictionary = np.unique(list(basket1) + list(basket2))
        vocab_len_ = len(dictionary)
        product2ind = dict(zip(dictionary, np.arange(vocab_len_)))

        dictionary_vecs = self.model.wv.vectors[[x for x in dictionary]]
        distance_matrix = squareform(pdist(dictionary_vecs))

        if np.sum(distance_matrix) == 0.0:
            return float('inf')

        def nbow(document):
            bow = np.zeros(vocab_len_, dtype=np.float32)
            for d in document:
                bow[product2ind[d]] += 1.
            return bow / len(document)

        d1 = nbow(basket1)
        d2 = nbow(basket2)

        return ot.emd2(d1, d2, distance_matrix)

    def remove_products_wo_embeddings(self, all_baskets, user_ids):
        all_baskets_filtered = []
        new_user_ids = []
        for (s, u_id) in zip(all_baskets, user_ids):
            s_cp = []
            for b in s:
                b_cp = [x for x in b if x in self.model.wv.index_to_key]
                if len(b_cp) > 0:
                    s_cp.append(b_cp)
            if len(s_cp) > 0:
                all_baskets_filtered.append(s_cp)
                new_user_ids.append(u_id)
        return all_baskets_filtered, new_user_ids