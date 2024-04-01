from cnsp_model.data_preprocessing import feature_extraction, handle_over_fitting, product_to_vec
from cnsp_model.embedding_wrapper import EmbeddingWrapper
from cnsp_model.basket_constructor import BasketConstructor
from cnsp_model.helper_functions import nested_change, remove_products_which_are_uncommon, remove_short_baskets, split_data
import pandas as pd
from cnsp_model.knn_dtw import KnnDtw
from cnsp_model.meta_prophet import predict
import numpy as np

def run(df):
    full_df = df
    final_df = full_df
    # final_df = handle_over_fitting(full_df)
    orders_df = feature_extraction(final_df)
    product_to_vec_model = product_to_vec(final_df)

    embedding_wrapper = EmbeddingWrapper(product_to_vec_model)
    bc = BasketConstructor(orders_df, final_df)
    ub_basket = bc.get_baskets()
    user_ids = ub_basket.user_id.values.tolist()
    all_baskets = ub_basket.basket.values
    all_baskets = nested_change(list(all_baskets), str)
    all_baskets, user_ids = embedding_wrapper.remove_products_wo_embeddings(all_baskets, user_ids)
    all_baskets, user_ids = remove_products_which_are_uncommon(all_baskets, user_ids)
    all_baskets, user_ids = remove_short_baskets(all_baskets, user_ids)
    all_baskets = nested_change(all_baskets, embedding_wrapper.lookup_ind_f)

    max_length = max(len(basket) for basket in all_baskets)
    all_baskets_padded = [basket + [] * (max_length - len(basket)) for basket in all_baskets]
    all_baskets_df = pd.DataFrame(all_baskets_padded, columns=[f'item_{i}' for i in range(max_length)])
    all_baskets_array = all_baskets_df.astype(str).agg(', '.join, axis=1)
    all_baskets_df = pd.DataFrame(all_baskets_array, columns=['basket'])
    all_baskets_df['user_id'] = user_ids

    train_ub, val_ub_input, val_ub_target, test_ub_input, test_ub_target, val_user, test_user = split_data(all_baskets_df)
    train_ub = [list(filter(lambda x: x is not None, sublist)) for sublist in train_ub]
    val_ub_input = [list(filter(lambda x: x is not None, sublist)) for sublist in val_ub_input]

    # Item prediction using KNN-DTW
    knndtw = KnnDtw(n_neighbors=[5])
    preds_all, distances = knndtw.predict(train_ub, val_ub_input, embedding_wrapper.basket_dist_EMD, 
                                          embedding_wrapper.basket_dist_REMD)

    preds_all = preds_all
    distances = distances[0]

    final_pred_df = pd.DataFrame({'User': val_user, 'Pred_Basket': preds_all[0], 'distances': distances})
    target_df = pd.DataFrame({'User': val_user, 'Basket': val_ub_target})

    emd_df = embedding_wrapper.word_index_df
    emd_df["product_id"] = emd_df["product_id"].astype(str)

    final_pred__list = final_pred_df['Pred_Basket'].to_list()
    final_target__list = target_df['Basket'].to_list()

    final_pred_df['Basket'] = final_pred__list
    target_df['Basket'] = final_target__list

    new_df = final_pred_df.explode('Basket').reset_index(drop=True)
    new_target_df = target_df.explode('Basket').reset_index(drop=True)

    new_df['product_id'] = new_df['Basket'].map(emd_df.set_index('emb_id')['product_id'])
    new_target_df['product_id'] = new_target_df['Basket'].map(emd_df.set_index('emb_id')['product_id'])
    new_basket_df = new_df.groupby(['User', 'distances'])['product_id'].apply(list).reset_index()

    # Quantity and date prediction using meta prophet
    result_df = predict(new_basket_df, final_df)
    result_df = result_df[result_df['quantity'] > 0]
    result_df['quantity'] = result_df['quantity'].apply(np.ceil).astype(int)

    return result_df