import pickle
import pandas as pd

pickled_model = pickle.load(open('model/finalized_model.sav', 'rb'))

def prediction(df):
    print("predict df:", df)
    
    df_code = pd.read_excel('model/zipcode_be.xlsx')
    df['code'] = df['zip_code']
    df['code'] = df['code'].astype(int)
    df = df.merge(df_code, on='code', how='left')
    pred = pickled_model.predict(df.drop(['full_address','property_type', 'name', 'province'], axis=1))
    print('Predicted price:', pred)
    
    return pred
    