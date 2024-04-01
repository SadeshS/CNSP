import pandas as pd
from math import ceil
import gensim

def feature_extraction(df: pd.DataFrame):
    orders = df.groupby('order_id').apply(lambda x: x.drop_duplicates(subset=['user_id'])).reset_index(drop=True)
    orders = orders.drop(["product_id","quantity"],axis =1)
    orders['date'] = pd.to_datetime(orders['date'])
    orders.sort_values(by=['user_id', 'date', 'order_id'], inplace=True)
    orders['days_since_prior_order'] = orders.groupby('user_id')['date'].diff().dt.days
    orders['days_since_prior_order'] = orders.groupby('order_id')['days_since_prior_order'].transform('first')
    orders['days_since_prior_order'].fillna(0, inplace=True)

    orders.sort_values(by=['user_id', 'date', 'order_id'], inplace=True)
    orders['order_number'] = 0 
    current_customer = None
    current_invoice = None
    order_number = 0
    for index, row in orders.iterrows():
        if row['user_id'] != current_customer:
            current_customer = row['user_id']
            current_invoice = None
            order_number = 0
        if row['order_id'] != current_invoice:
            current_invoice = row['order_id']
            order_number += 1
        
        orders.at[index, 'order_number'] = order_number
    
    return orders

def handle_over_fitting(df: pd.DataFrame):
    order_counts = df.groupby('user_id')['order_id'].nunique()

    users_with_few_orders = order_counts[order_counts < 10].index
    data_filtered = df[~df['user_id'].isin(users_with_few_orders)]

    total_orders_per_user = data_filtered.groupby('user_id')['order_id'].nunique()
    overall_average_orders_per_user = total_orders_per_user.mean()
    overall_average_orders_per_user = ceil(overall_average_orders_per_user)

    users_with_many_orders = order_counts[order_counts > (80 if overall_average_orders_per_user > 80 else overall_average_orders_per_user)].index
    data_many_orders_filtered = pd.DataFrame()
    for user_id in users_with_many_orders:
        user_data = data_filtered[data_filtered['user_id'] == user_id]
        latest_orders = user_data.sort_values(by='date', ascending=False)['order_id'].unique()[:80 if overall_average_orders_per_user > 80 else overall_average_orders_per_user]
        user_data_filtered = user_data[user_data['order_id'].isin(latest_orders)]
        data_many_orders_filtered = pd.concat([data_many_orders_filtered, user_data_filtered], ignore_index=True)

    final_data = pd.concat([data_filtered[~data_filtered['user_id'].isin(users_with_many_orders)], data_many_orders_filtered], ignore_index=True)
    return final_data

def product_to_vec(df: pd.DataFrame):
    df["product_id"] = df["product_id"].astype(str)
    products = df.groupby("order_id").apply(lambda order: order['product_id'].tolist())
    sentences = products.values
    model = gensim.models.Word2Vec(sentences, window=5, min_count=50, workers=4)
    return model
