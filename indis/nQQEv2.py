import pandas as pd 
import numpy as np
import copy

try:
    from .osci import rsi
except:
    from osci import rsi

def nz(x):
    if x is np.nan or x is None:
        return 0
    return x

def calcVals(row):
    index = row.name
    pre = int(index)-1

    try:
        wwma = wwalpha*row['TR'] + (1-wwalpha)*outData['WWMA'][pre]
    except:
        outData['QQES'][index] = 0
        return

    outData['WWMA'][index] = wwma

    atrrsi = wwalpha*wwma + (1-wwalpha)*outData['ATRRSI'][pre]
    outData['ATRRSI'][index] = atrrsi

    qup = row['QQEF'] + atrrsi*4.236
    qdn = row['QQEF'] - atrrsi*4.236

    outData['QUP'][index] = qup
    outData['QDN'][index] = qdn

    # current vals
    qqef = row['QQEF']
    qqes = row['QQES']

    # previous vals
    p_qqef = outData['QQEF'][pre]
    p_qup = outData['QUP'][pre]
    p_qdn = outData['QDN'][pre]
    p_qqes = outData['QQES'][pre]

    if qup < p_qqes :
        outData['QQES'][index] = qup 
    else:
        if qqef > p_qqes and p_qqef < p_qqes:
            outData['QQES'][index] = qdn
        else:
            if qdn > p_qqes:
                outData['QQES'][index] = qdn
            else :
                if qqef < p_qqes and p_qqef > p_qqes :
                    outData['QQES'][index] = qup
                else:
                    outData['QQES'][index] = p_qqes

def nQQE(df, rsi_l=14, ssf=5):
    RSI = rsi(df['close'], rsi_l)
    RSII = RSI.ewm(span = ssf).mean()
    TR = abs(RSII.diff())
    global wwalpha
    wwalpha = 1/rsi_l

    global outData    
    outData = pd.DataFrame({'TR': TR})
    outData['WWMA'] = 0.0
    outData['ATRRSI'] = 0.0
    outData['QQEF'] = RSII
    outData['QQES'] = 0.0
    outData['QUP'] = 0.0
    outData['QDN'] = 0.0
    outData['openTime'] = df['openTime']

    # outData = outData.fillna(0)
    outData = outData.dropna().reset_index(drop=True)

    

    outData.apply(calcVals, axis=1)
    # print(outData['ATRRSI'])
    return outData.drop(['QDN', 'QUP', 'TR', 'WWMA', 'ATRRSI'], axis=1)

if __name__ == "__main__":
    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)
    result = nQQE(df)

    diff = result['QQEF']-result['QQES']

    print(diff)