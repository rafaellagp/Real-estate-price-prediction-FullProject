import pandas as pd

def preprocessing(df):
    df['building_state'] = (df['building_state']).replace({'GOOD': 0, 'NEW': 1, 'TO RENOVATE': 0, 
    'JUST RENOVATED': 0, 'TO REBUILD':0})
    u = df.select_dtypes(bool)
    df[u.columns] = u.astype(int)
    return df