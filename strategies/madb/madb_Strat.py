import pandas as pd

from backtest import bt
from indis.madb import madb

if __name__ == "__main__":
    import getData
    candles = getData.getCandles(
        symbol="BTCUSDT", 
        leng='6 month', 
        time=15, 
        klineType="FUTURES"
    )

    df = pd.DataFrame(candles)
    df = df.drop([7,8,9,10,11], axis=1)
    df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']
    
    # df = pd.read_csv('test/testData.csv') 

    strat = bt(df, portfolio=10)
    strat.leverage = 10

    outData = madb(strat.candles,length=20)
    strat.setLineSeriesData(outData)

    strat.initNumPy()
    strat.defineOrder('open > upper1 and close < upper1', "low < basis", longFlag=False)
    strat.defineOrder('open < lower1 and close > lower1', 'high > basis')

    # strat.defineOrder('open < basis and close > basis', 'high > upper1')
    # strat.defineOrder('open > basis and close < basis', 'low < lower1', longFlag=False)



   
    # print(outData)
    # strat.plotCandles()
    # strat.plotLineSeries()
    # strat.plotOrders()
    print(strat.portfolio)
    df = strat.getOrderList()
    df.to_csv('strategies/madb/orders.csv')
    # # # print(strat.candleColumns)
    # strat.showPlot(file='strategies/madb/plot.html')
    