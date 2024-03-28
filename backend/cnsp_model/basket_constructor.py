import pandas as pd

class BasketConstructor(object):
    def __init__(self, orders_df, full_df):
        self.orders_df = orders_df
        self.full_df = full_df
    
    def get_orders(self):
        orders = self.orders_df
        orders = orders.fillna(0.0)
        orders['days'] = orders.groupby(['user_id'])['days_since_prior_order'].cumsum()
        orders['days_last'] = orders.groupby(['user_id'])['days'].transform(max)
        orders['days_up_to_last'] = orders['days_last'] - orders['days']
        del orders['days_last']
        del orders['days']
        return orders
    
    def get_orders_items(self):
        orders_products = self.full_df
        return orders_products
    
    def get_users_orders(self):
        orders = self.get_orders()
        order_products = self.get_orders_items()
        users_orders = pd.merge(order_products, orders[['user_id', 'order_id', 'order_number', 'days_up_to_last']], 
                    on = ['order_id', 'user_id'], how = 'left')
        return users_orders
    
    def get_users_products(self):
        users_products = self.get_users_orders()[['user_id', 'product_id']].drop_duplicates()
        users_products['product_id'] = users_products.product_id.astype(int)
        users_products['user_id'] = users_products.user_id.astype(int)
        users_products = users_products.groupby(['user_id'])['product_id'].apply(list).reset_index()
        return users_products
    
    def get_baskets(self):
        up = self.get_users_orders().sort_values(['user_id', 'order_number', 'product_id'], ascending = True)
        uid_oid = up[['user_id', 'order_number']].drop_duplicates()
        up = up[['user_id', 'order_number', 'product_id']]
        up_basket = up.groupby(['user_id', 'order_number'])['product_id'].apply(list).reset_index()
        up_basket = pd.merge(uid_oid, up_basket, on = ['user_id', 'order_number'], how = 'left')
        up_basket = up_basket.sort_values(['user_id', 'order_number'], ascending = True).groupby(['user_id'])['product_id'].apply(list).reset_index()
        up_basket.columns = ['user_id', 'basket']
        return up_basket
        
    def get_item_history(self, none_idx = 49689):
        up = self.get_users_orders().sort_values(['user_id', 'order_number', 'product_id'], ascending = True)
        item_history = up.groupby(['user_id', 'order_number'])['product_id'].apply(list).reset_index()
        item_history.loc[item_history.order_number == 1, 'product_id'] = item_history.loc[item_history.order_number == 1, 'product_id'] + [none_idx]
        item_history = item_history.sort_values(['user_id', 'order_number'], ascending = True)
        item_history['product_id'] = item_history.groupby(['user_id'])['product_id'].transform(pd.Series.cumsum)
        item_history['product_id'] = item_history['product_id'].apply(set).apply(list)
        item_history = item_history.sort_values(['user_id', 'order_number'], ascending = True)
        item_history['product_id'] = item_history.groupby(['user_id'])['product_id'].shift(1)
        for row in item_history.loc[item_history.product_id.isnull(), 'product_id'].index:
            item_history.at[row, 'product_id'] = [none_idx]
        item_history = item_history.sort_values(['user_id', 'order_number'], ascending = True).groupby(['user_id'])['product_id'].apply(list).reset_index()
        item_history.columns = ['user_id', 'history_items']
        return item_history 