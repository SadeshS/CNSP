from collections import Counter
from sklearn.model_selection import train_test_split
import ast

def nested_change(item, func):
    if isinstance(item, list):
        return [nested_change(x, func) for x in item]
    return func(item)

def remove_products_which_are_uncommon(all_baskets, user_ids, max_num=500):
    p = []
    for s in all_baskets:
        for b in s:
            p.extend(b)
    product_counter = Counter(p)
    most_common_products = [x for x, _ in product_counter.most_common(max_num)]
    new_user_ids = []
    all_baskets_filtered = []
    for (s, u_id) in zip(all_baskets, user_ids):
        s_cp = []
        for b in s:
            b_cp = [x for x in b if x in most_common_products]
            if len(b_cp) > 0:
                s_cp.append(b_cp)
        if len(s_cp) > 0:
            new_user_ids.append(u_id)
            all_baskets_filtered.append(s_cp)
    return all_baskets_filtered, new_user_ids

def remove_short_baskets(all_baskets, user_ids, l_b = 5, l_s = 10):
    new_user_ids = []
    all_baskets_filtered = []
    for (s, u_id) in zip(all_baskets, user_ids):
        s_cp = []
        for b in s:
            if len(b) > l_b:
                s_cp.append(b)
        if len(s_cp) > l_s:
            new_user_ids.append(u_id)
            all_baskets_filtered.append(s_cp)
    return all_baskets_filtered, new_user_ids

def convertType(item):
    return [ast.literal_eval(x) for x in item]

def split_data(all_baskets):
    users = []
    train_ub, test_ub = train_test_split(all_baskets, test_size=0.05, random_state=0)
    train_ub, val_ub = train_test_split(train_ub, test_size=0.05, random_state=0)
    
    train_user_id = train_ub.user_id.values.tolist()
    test_user_id = test_ub.user_id.values.tolist()
    val_user_id = val_ub.user_id.values.tolist()
    
    users.append(train_user_id)
    users.append(test_user_id)
    users.append(val_user_id)
    
    train_ub = convertType(train_ub['basket'])
    
    test_ub = convertType(test_ub['basket'])
    
    val_ub = convertType(val_ub['basket'])
    test_ubC = [list(filter(lambda x: x is not None, sublist)) for sublist in test_ub]
    val_ubC = [list(filter(lambda x: x is not None, sublist)) for sublist in val_ub]

    test_ub_input = [x[:-1] for x in test_ubC]
    test_ub_target = [x[-1] for x in test_ubC]
    
    val_ub_input = [x[:-1] for x in val_ubC]
    val_ub_target = [x[-1] for x in val_ubC]
    
    return train_ub, val_ub_input, val_ub_target, test_ub_input, test_ub_target, val_user_id, test_user_id