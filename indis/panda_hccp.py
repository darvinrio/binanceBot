import pandas as pd 
import numpy as np 

def rma(ser):
    ser = ser.ewm(alpha=1/Alpha).mean().reset_index(drop=True)
    val = ser[Alpha-1]
    return val

def true_range(row):
    return max(
        row['high'] - row['low'],
        abs(row['high'] - row['open']),
        abs(row['open'] - row['low'])
    )

def HCCP(df, scl=10, mcl=30, scm=1.0, mcm=3.0):

    global Alpha
    scl = int(scl/2)
    mcl = int(mcl/2)

    Alpha = scl
    ma_scl = df['close'].rolling(scl).apply(rma)
    Alpha = mcl
    ma_mcl = df['close'].rolling(mcl).apply(rma)

    tr = df.apply(true_range, axis=1)

    Alpha = scl
    scm_off = tr.rolling(scl).apply(rma)
    Alpha = mcl
    mcm_off = tr.rolling(mcl).apply(rma)

    scl_2=int(scl/2)
    mcl_2=int(mcl/2)

    shifted_ma_scl = ma_scl.shift(scl_2)
    shifted_ma_mcl = ma_mcl.shift(mcl_2)

    sct = shifted_ma_scl + scm_off
    scb = shifted_ma_scl - scm_off
    mct = shifted_ma_mcl + mcm_off
    mcb = shifted_ma_mcl - mcm_off

    out = pd.DataFrame({
        'openTime' : df['openTime'],
        'sct' : sct,
        'scb' : scb,
        'mct' : mct,
        'mcb' : mcb
    })

    return out

if __name__ == "__main__":

    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)

    out = HCCP(df)

    print(out)