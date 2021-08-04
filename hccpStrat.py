import pandas as pd 

from backtest import bt
from indis.hccp import getHCCP

if __name__ == "__main__":
    # import getData
    # candles = getData.getCandles(
    #     symbol="BTCUSDT", 
    #     leng='1 day', 
    #     time=1, 
    #     klineType="FUTURES"
    # )

    # df = pd.DataFrame(candles)
    # df = df.drop([7,8,9,10,11], axis=1)
    # df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']
    
    df = pd.read_csv('test/testData.csv') 

    strat = bt(df, portfolio=10)

    outData = getHCCP(strat.candles)

    print(outData)