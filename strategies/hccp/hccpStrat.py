import pandas as pd 

from backtest import bt
from indis.panda_hccp import HCCP
from plotter import plotlyPlotter as plt 

if __name__ == "__main__":
    import getData
    candles = getData.getCandles(
        symbol="BTCUSDT", 
        leng='1 day', 
        time=1, 
        klineType="FUTURES"
    )

    df = pd.DataFrame(candles)
    df = df.drop([7,8,9,10,11], axis=1)
    df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']
    
    for column in df:
        if column == 'openTime' or column == 'closeTime' :
            continue
        df[column] = pd.to_numeric(df[column], downcast="float")
         

    # df = pd.read_csv('test/testData.csv') 

    fig = plt()
    fig.addCandles(df)

    hccpData = HCCP(df)
    fig.addLineSeries(hccpData)

    fig.showPlot()