import numpy as np
import pandas as pd

try:
    from .strip import strip 
except:
    from strip import strip 

def atrVal(arr): # arr = [[h, l, c]]
    tr = np.zeros(len(arr))

    for i in range(len(arr)) :
        hl = arr[i][0] - arr[i][1]
        if i != 0 :
            hc = abs(arr[i][0] - arr[i-1][2])
            lc = abs(arr[i][1] - arr[i-1][2])
        else:
            hc = 0
            lc = 0
        
        tr[i] = max(hl, hc, lc)

    return np.average(tr)

def atr(df, lookback):

    highSer = df['high']
    high = ((highSer.to_numpy()).transpose())

    lowSer = df['low']
    low = ((lowSer.to_numpy()).transpose())

    closeSer = df['close']
    close = ((closeSer.to_numpy()).transpose())

    hlc = np.stack((high,low,close), axis=1)

    l = len(hlc)
    out = np.array([])

    for i in range(l):
        arr = strip(hlc, i=i, n=lookback)
        if arr is None:
            out = np.append(out, np.nan)
        else:
            nArr = arr.reshape(int(len(arr)/3), 3)
            atr = atrVal(nArr)
            out = np.append(out,atr)

    
    return pd.DataFrame({'atr'+str(lookback) : out})


if __name__ == "__main__":

    # a = np.array([[3,1,2],[6,4,5],[9,7,8]])

    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)

    #atr(df,10)

    out = atr(df,10) 
    print(out)