import pandas as pd
from prophet import Prophet

def preprocess_data(retail_dataframe, cust_list):
    df = retail_dataframe[['date', 'order_id', 'user_id', 'product_id', 'quantity']]
    df = df[df['user_id'].isin(cust_list)]
    df = df.dropna()
    df['date'] = df['date'].astype(str)
    df['user_id'] = df['user_id'].astype(str)
    df['product_id'] = df['product_id'].astype(str)
    df['Date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.strftime('%Y/%m/%d')
    df['Date'] = pd.to_datetime(df['date'])
    df = df.groupby(['Date', 'order_id', 'user_id', 'product_id'])['quantity'].apply(sum).reset_index()
    df = df[['Date', 'user_id', 'product_id', 'quantity']].rename({'Date': 'ds', 'quantity': 'y'}, axis='columns')
    return df

def predict(pred_df, full_df):
    cust_list = pred_df['User'].tolist()
    fullcsv_df = full_df
    
    train_df = preprocess_data(fullcsv_df, cust_list)
    FINAL_DF = pd.DataFrame()
    
    for cust_id in cust_list:
        prod_list = pred_df.loc[pred_df['User'] == cust_id, 'product_id'].iloc[0]
        def_new = train_df[train_df['user_id'] == str(cust_id)]
        def_new = def_new[def_new['product_id'].isin(prod_list)]
        split_group = def_new.groupby('product_id')
        splits = [split_group.get_group(x) for x in split_group.groups]
        
        for p_df in splits:
            productcode = p_df['product_id'].iloc[0]
            
            if(len(p_df) > 1):
                product_df = p_df[['ds', 'y']]
                last_date = product_df['ds'].max().strftime('%Y-%m-%d')
                m = Prophet(interval_width=0.95)
                m.fit(product_df, algorithm='lbfgs')
                future = m.make_future_dataframe(periods=1, freq='m', include_history=False)
                forecast = m.predict(future)
                forecast = forecast[['yhat', 'ds']]
                forecast['user_id'] = cust_id
                forecast['product_id'] = productcode
                forecast = forecast.rename(columns={'yhat': 'quantity', 'ds': 'date'})
                
                FINAL_DF = pd.concat([FINAL_DF, forecast], ignore_index=True)
    return FINAL_DF