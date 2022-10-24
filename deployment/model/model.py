from gettext import npgettext
from pyexpat import features
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import ensemble

import pickle

def remove_outliers(df, column, zscore = 3):
    upper_limit = df[column].mean() + zscore * df[column].std()
    lower_limit = df[column].mean() - zscore * df[column].std()
    normal_df = df[(df[column] < upper_limit) & (df[column] > lower_limit)]
    return normal_df

def train_model(df_features, labels):
    X_train, X_test, y_train, y_test = train_test_split(df_features, labels, test_size = 0.3,random_state=2)
    clf = ensemble.GradientBoostingRegressor(n_estimators=400,max_depth=6,min_samples_split=2,learning_rate=0.1,loss= 'squared_error')
    clf.fit(X_train,y_train)
    
    # save the model to disk
    filename = 'model/finalized_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    # score = clf.score(X_test,y_test)
    # pred = clf.predict(X_test)
    # print('Score :', score)
    # print('Predicted price:', pred)
    
def preprocess_data():
    df = pd.read_csv('/Users/rafaellaporto/BeCode/challenge-api-deployment/model/data_model.csv')
    df_code = pd.read_excel('/Users/rafaellaporto/BeCode/challenge-api-deployment/model/zipcode_be.xlsx')

    df = df.rename({'Unnamed: 0': 'id'}, axis=1)

    df['code'] = df['zip_code']
    df_code['code']=df_code['code'].astype(int)
    df['code']=df['code'].astype(int)
    df = df.merge(df_code, on='code', how='left')
    df = df.drop_duplicates(subset="id")
    df = df.dropna()

    df['building_state'] = (df['building_state']).replace({'good': 0, 'to renovate': 0, 'as new': 1, 'to be done up': 0, 
    'just renovated': 0, 'to restor':0, 'to rebuild':0 , 'not mentioned': 0})
    df = remove_outliers(df, 'price')
    df = df.drop(['id','full_address','name','province'],axis=1)

    df_features = df.drop(["property_type", 'price'],axis=1)
    return df_features, df['price']

########################
# CODE
########################

if __name__ == "__main__":
    df_features, prices = preprocess_data()
    train_model(df_features, prices)

    # X_train, X_test, y_train, y_test = train_test_split(df_features, prices, test_size = 0.3,random_state=2)
    # clf = ensemble.GradientBoostingRegressor(n_estimators=400,max_depth=6,min_samples_split=2,learning_rate=0.1,loss= 'squared_error')
    # clf.fit(X_train,y_train)
    # score = clf.score(X_test,y_test)
    # exemple_data = {'area' :[110],'rooms_number' :[3],'zip_code' :[5080],'land_area':[824],'garden':[0],'garden_area':[0],'equipped_kitchen':[0],'swimming_pool':[0],'furnished':[0],'open_fire':[0],'terrace':[0],'terrace_area':[0],'facades_number':[4],'building_state':[1],'code':[5080],'lat':[5038930954],'lng':[482362925]}
    # test_df = pd.DataFrame(exemple_data)
    # pred = clf.predict(test_df)
    # print('Score :', score)
    # print('Predicted price:', pred)
    # print('Real price: €215,000')
