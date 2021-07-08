import ma
import volat
import pandas as pd
import numpy as np

def nz(a,b):
    if a is np.nan or a is None:
        return b
    return a

def getHCCP(df, scl=10, mcl=30, scm=1.0, mcm=3.0): # hlc = [h, l, c]

    scl = int(scl/2)
    mcl = int(mcl/2)

    ma_scl = ma.rma(df, scl) 
    ma_mcl = ma.rma(df, mcl) 

    scm_off = scm*(volat.atr(df,scl))
    mcm_off = mcm*(volat.atr(df,mcl))

    # print(df)

    # df = pd.concat([ma_scl, ma_mcl, scm_off, mcm_off], axis=1)

    scl_2 = int(scl/2)
    mcl_2 = int(mcl/2)

    ma_scl_2 = ma_scl.shift(periods = -scl_2)
    ma_scl_2.columns = [list(ma_scl_2.columns.values)[0]+'shifted']

    ma_mcl_2 = ma_mcl.shift(periods = -mcl_2)
    ma_mcl_2.columns = [list(ma_mcl_2.columns.values)[0]+'shifted']
    
    df2 = pd.concat([ma_scl_2, ma_mcl_2, scm_off, mcm_off], axis=1)
    cols = list(df2.columns.values)
    # cols = [rma1, rma2, atr1, atr2]
    df2[cols[0]] = df2[cols[0]].mask(pd.isnull, df['close'])
    df2[cols[1]] = df2[cols[1]].mask(pd.isnull, df['close'])

    df['sct'] = df2[cols[0]] + df2[cols[2]]
    df['scb'] = df2[cols[0]] - df2[cols[2]]
    df['mct'] = df2[cols[1]] + df2[cols[3]]
    df['mcb'] = df2[cols[1]] - df2[cols[3]]

    # df['sct']=df['sct'].mask(pd.isnull, df['close'])
    # df['scb']=df['scb'].mask(pd.isnull, df['close'])
    # df['mct']=df['mct'].mask(pd.isnull, df['close'])
    # df['mcb']=df['mcb'].mask(pd.isnull, df['close'])


    print(df)

if __name__ == "__main__":

    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)

    getHCCP(df)
