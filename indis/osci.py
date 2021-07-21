import pandas as pd 
import numpy as np

def rsi(s, l=14):

    delta = s.diff()

    upVals = delta.clip(lower = 0)
    downVals = -1*delta.clip(upper = 0)

    upEMA = upVals.ewm(com = l-1, adjust=False).mean()
    downEMA = downVals.ewm(com = l-1, adjust=False).mean()

    rsVals = upEMA/downEMA

    rsiVals = 100 - (100/(1 + rsVals))
    rsiVals.name = 'RSI_'+str(l)

    for i in range(l):
        rsiVals[i] = np.nan

    return rsiVals

if __name__ == "__main__":
    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)

    rsi = rsi(df['close'])

    # rsi[1] = np.nan

    print(rsi)

    oversold = rsi[rsi > 70]

    print(oversold)

    # print(type(df['close']))
    
