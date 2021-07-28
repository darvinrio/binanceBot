import pandas as pd 
import numpy as np
import copy

def madb(df, length=20, mult=2):
    logReturn = np.log(df['close']/df['open'])
    logReturn.name = 'logReturn'

    sma = df['close'].rolling(length).mean()
    sma.name = 'sma'

    logSMAlength = 3
    logSMA = (logReturn*df['close']).rolling(logSMAlength).mean()
    logSMA.name = 'logSMA'

    basisLine = sma + logSMA

    dev = logReturn.rolling(length).std()
    visibleDev = dev*df['close']*mult

    upper1 = basisLine + visibleDev
    lower1 = basisLine - visibleDev    
    upper2 = basisLine + visibleDev*2
    lower2 = basisLine - visibleDev*2

    outdf = pd.DataFrame({
        'openTime' : df['openTime'],
        'basis' : basisLine,
        'upper1' : upper1,
        'lower1' : lower1,
        'upper2' : upper2,
        'lower2' : lower2,
    })

    return outdf


if __name__ == "__main__":
    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)
    result = madb(df)

    # diff = result['QQEF']-result['QQES']

    print(result)