import pandas as pd 
import numpy as np
import copy

from osci import rsi

def prevVal(x):
    return x.reset_index(drop=True)[0]

def nz(x):
    if x is np.nan or x is None:
        return 0
    return x

def nQQE(df, rsi_l=14, ssf=5):
    RSI = rsi(df['close'], rsi_l)
    RSII = RSI.ewm(span = ssf).mean()
    TR = abs(RSII.diff())

    df['zero'] = 0.0
    wwalpha = 1/rsi_l
    WWMA = copy.deepcopy(df['zero'])
    ATRRSI = copy.deepcopy(df['zero'])
    
    WWMA = wwalpha*TR + (1-wwalpha)*WWMA.rolling(2).apply(prevVal)
    ATRRSI = wwalpha*WWMA + (1-wwalpha)*ATRRSI.rolling(2).apply(prevVal)
    QQEF = copy.deepcopy(RSII)

    QUP = QQEF+ATRRSI*4.236
    QDN = QQEF-ATRRSI*4.236

    QQES = copy.deepcopy(df['zero'])

    DF = pd.DataFrame({
        'QQEF': QQEF,
        'QUP' : QUP,
        'QDN' : QDN,
        'QQES': QQES
    })
    print(DF)

    def calcQQES(row):
        index = row.name
        pre = int(index)-1

        # current vals
        qqef = row['QQEF']
        qup = row['QUP']
        qdn = row['QDN']
        qqes = row['QQES']
    
        # previous vals
        try:
            p_qqef = nz(DF['QQEF'][pre])
            p_qup = nz(DF['QUP'][pre])
            p_qdn = nz(DF['QDN'][pre])
            p_qqes = nz(DF['QQES'][pre])
        except:
            return np.nan


        if qup < p_qqes :
            return qup 
        else:
            if qqef > p_qqes and p_qqef < p_qqes:
                return qdn
            else:
                if qdn > p_qqes:
                    return qdn
                else :
                    if qqef < p_qqes and p_qqef > p_qqes :
                        return qup
                    else:
                        return p_qqes

    DF['QQES'] = DF.apply(calcQQES, axis=1)
    DF['openTime'] = df['openTime']

    return DF

if __name__ == "__main__":
    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)
    print(nQQE(df))
