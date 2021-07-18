import pandas as pd 
import numpy as np 

try:
    from .ma import wmaDF
except:
    from ma import wmaDF

def lazyLine(df, l=15):
    w1 = 0
    w2 = 0
    w3 = 0

    w = l / 3

    if l>3 :
        w2 = int(np.round(w))
        w1 = int(np.round((l-w2)/2))
        w3 = int((l-w2)/2)

        L1 = wmaDF(df, w1)
        L2 = wmaDF(L1, w2, column='wma10')
        L3 = wmaDF(L2, w3, column='wma10')

        return pd.concat([L3, df['openTime']], axis=1)
    
    else :
        return df

if __name__ == "__main__":
    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)
    
    print(lazyLine(df,15))
