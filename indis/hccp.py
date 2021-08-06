
try:
    from .ma import rma
    from .volat import atr
except:
    from ma import rma
    from volat import atr    
import pandas as pd
import numpy as np

def nz(a,b):
    if a is np.nan or a is None:
        return b
    return a

def getHCCP(df, scl=10, mcl=30, scm=1.0, mcm=3.0): # hlc = [h, l, c]

    scl = int(scl/2)
    mcl = int(mcl/2)

    ma_scl = rma(df, scl) 
    ma_mcl = rma(df, mcl) 

    scm_off = scm*(atr(df,scl))
    mcm_off = mcm*(atr(df,mcl))

    # print(df)

    # df = pd.concat([ma_scl, ma_mcl, scm_off, mcm_off], axis=1)

    scl_2 = int(scl/2)
    mcl_2 = int(mcl/2)

    ma_scl_2 = ma_scl.shift(periods = scl_2)
    ma_scl_2.columns = [list(ma_scl_2.columns.values)[0]+'shifted']

    ma_mcl_2 = ma_mcl.shift(periods = mcl_2)
    ma_mcl_2.columns = [list(ma_mcl_2.columns.values)[0]+'shifted']
    
    df2 = pd.concat([
        ma_scl_2, ma_mcl_2, scm_off, mcm_off#, ma_mcl, ma_scl
    ], axis=1)
    
    cols = list(df2.columns.values)

    out = pd.DataFrame()
    out['openTime'] = df['openTime']
    out['sct'] = df2[cols[0]] + df2[cols[2]]
    out['scb'] = df2[cols[0]] - df2[cols[2]]
    out['mct'] = df2[cols[1]] + df2[cols[3]]
    out['mcb'] = df2[cols[1]] - df2[cols[3]]
    
    return out

if __name__ == "__main__":

    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)

    out = getHCCP(df)

    # for row in out.iterrows():
    #     print(row)

    # out = out.dropna().reset_index(drop=True)
    # out = out
    print(out)
