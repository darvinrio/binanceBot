import numpy as np
import pandas as pd
try:
    from .strip import strip 
except:
    from strip import strip 

def rmaVal(arr, l): # returns rma for give array and length
    a = 1/l
    if len(arr) == 1 :
        return arr[0]
    else :
        dArr = np.delete(arr,0)
        prev = rmaVal(dArr, l)
        return (a*prev)+((1-a)*arr[0])

def drmaVal(arr, l):
    a = 1/l
    if len(arr) == 1 :
        return arr[0]
    else :
        dArr = np.delete(arr,0)
        prev = drmaVal(dArr, l-1)
        return (a*prev)+((1-a)*arr[0])

def rma(df, lookback):
    closeSer = df['close']
    close = ((closeSer.to_numpy()).transpose())
    
    l = len(close)

    out = np.array([])

    for i in range(l) :
        arr = strip(close, i, lookback)
        if arr is None:
            out = np.append(out, np.nan)
        else:
            rma = rmaVal(arr, lookback)
            out = np.append(out, rma)

    return pd.DataFrame({'rma'+str(lookback) : out})

def ma(df, l):
    close = df['close']
    ma = close.rolling(l).mean()
    print(ma.head(10))

def wma(arr, l):
    norm = 0.0
    sum = 0.0
    for i in range(l):
        weight = (l-i)*l
        norm += weight
        sum += arr[i]*weight
    return sum / norm

def wmaDF(df, l, column='close'):
    weights = np.arange(1,l+1)
    wma10 = df[column].rolling(l).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
    return pd.DataFrame({'wma10':wma10})

if __name__ == "__main__":
    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)

    # out = rma(df,10)
    # print(out.head(100))

    a = np.array([90.90,90.36,90.28,90.83,90.91])

    # df = pd.DataFrame({'close':a})
    print(wmaDF(df,10))

