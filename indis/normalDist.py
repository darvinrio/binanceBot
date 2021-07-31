import numpy as np 
import pandas as pd 
import scipy.stats as ss 

def __meanColor(row, posColor='green', negColor='red'):
    if row>=0 :
        return posColor
    else:
        return negColor 

def moments(df, length=20, mult=1.96):
    logReturn = np.log(df['close']/df['open'])*100

    std = logReturn.rolling(length).std(ddof = 0)
    meanLogReturn = logReturn.rolling(length).mean()

    upperBound = meanLogReturn + std
    lowerBound = meanLogReturn - std

    outDF = pd.DataFrame({
        'openTime' : df['openTime'],
        'logReturn' : logReturn,
        'meanLogReturn' : meanLogReturn,
        'upperBound' : upperBound,
        'lowerBound' : lowerBound
    })

    return outDF

def getMeanColorData(ser):
    return ser.apply(__meanColor)
    

if __name__ == "__main__":
    df = (pd.read_csv('../test/testData.csv')).drop('Unnamed: 0',axis=1)
    result = moments(df,20)

    # diff = result['QQEF']-result['QQES']
    logReturn = result['logReturn']

    color = getMeanColorData(logReturn)

    print(color)