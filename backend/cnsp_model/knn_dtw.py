import numpy as np
from tqdm import tqdm
from collections import Counter

class KnnDtw(object):    
    def __init__(self, n_neighbors):
        self.n_neighbors = n_neighbors  
        self.length_to_consider = 10
    
    def _spring_dtw_distance(self, ts_a, ts_b, best_for_ts_a, d, d_lower_bound):
        M, N = len(ts_a), len(ts_b)

        REMD_gen = map(d_lower_bound, [(i,j) for i in ts_a for j in ts_b])
        d_REMD_min = np.fromiter(REMD_gen, dtype=np.float32)

        if np.sum(d_REMD_min[np.argpartition(d_REMD_min, M)][:M]) > max(best_for_ts_a):
            return np.inf, ts_b[0]

        cost = np.inf * np.ones((M, N))

        d_mat = np.zeros((M,N))
        for i in range(M):
            for j in range(N):
                d_mat[i,j] = d((ts_a[i], ts_b[j]))

        cost[0, 0] = d((ts_a[0], ts_b[0]))
        for i in range(1, M):
            cost[i, 0] = cost[i-1, 0] + d_mat[i, 0]

        for j in range(1, N):
            cost[0, j] = d_mat[0, j]
            
        for i in range(1, M):
            w = 1.
            for j in range(1, N):
                choices = cost[i-1, j-1], cost[i, j-1], cost[i-1, j]
                cost[i, j] = min(choices) + w * d_mat[i,j]

        min_idx = np.argmin(cost[-1,:-1])
        return cost[-1,min_idx], ts_b[min_idx + 1]
  
    def _dist_matrix(self, x, y, d, d_lower_bound):
        x_s = [len(x)]
        y_s = [len(y)]
        dm = np.inf * np.ones((x_s[0], y_s[0])) 
        next_baskets = np.empty((x_s[0], y_s[0]), dtype=object)
        
        for i in tqdm(range(0, x_s[0])):
            max_length = max(len(seq) for seq in x[i])
            x[i] = [np.array(seq)[-max_length:] for seq in x[i]]

            best_dist = [np.inf] * max(self.n_neighbors)
            for j in range(0, y_s[0]):
                max_length_y = max(len(seq_y) for seq_y in y[j])
                y[j] = [np.array(seq_y)[-max_length_y:] for seq_y in y[j]]

                dist, pred = self._spring_dtw_distance(x[i], y[j], best_dist, d, d_lower_bound)
                if dist < np.max(best_dist):
                    best_dist[np.argmax(best_dist)] = dist               
                dm[i, j] = dist
                next_baskets[i, j] = pred
    
        return dm, next_baskets
        
        
    def predict(self, tr_d, te_d, d, d_lower_bound):
        dm, predictions = self._dist_matrix(te_d, tr_d, d, d_lower_bound)
        
        preds_total_l = []
        distances_total_l = []
        for k in self.n_neighbors:
            knn_idx = dm.argsort()[:, :k]
            preds_k_l = []
            distances_k_l = []
                
            for i in range(len(te_d)):
                preds = [predictions[i][knn_idx[i][x]] for x in range(knn_idx.shape[1])]
                distances = np.mean([dm[i][knn_idx[i][x]] for x in range(knn_idx.shape[1])])
                pred_len = int(np.mean([len(te_d[i][x]) for x in range(len(te_d[i]))]))
                preds = [x for x, y in Counter([n for s in preds for n in s]).most_common(pred_len)]                
                preds_k_l.append(preds)
                distances_k_l.append(distances)
            preds_total_l.append(preds_k_l)
            distances_total_l.append(distances_k_l)
            
        return preds_total_l, distances_total_l