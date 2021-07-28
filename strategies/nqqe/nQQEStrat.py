from binanceAPI import dAPI
from backtest import bt
import plotlyTest as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



import pandas as pd

class nqqeStrat(bt):

    def __init__(self, candles, portfolio=10):

        super().__init__(candles, portfolio)

        from indis.nQQE import nQQE
        self.nQQEdata = nQQE(self.candles)
        self.nQQEdata['s_QQEF'] = self.nQQEdata['QQEF'].shift()

        self.setLineSeriesData(self.nQQEdata)

        self.fig = make_subplots(
            rows=2, cols=1, 
            shared_xaxes=True,
            vertical_spacing=0,
            row_heights=[0.5, 0.5]
        )

        self.fig.update_layout(
            hovermode="x unified",
            dragmode='pan'
        )
        self.fig.update_xaxes(
            zeroline=False,
            # rangeslider_visible=False,
            showspikes=True, 
            spikemode='across', 
            spikesnap='cursor'
        )
        self.fig.update_yaxes(
            zeroline=False,
            fixedrange=False,
            showspikes=True, 
            spikemode='across', 
            spikesnap='cursor'
        )

    def plotCandles(self):
        df = self.candles
        self.fig.add_trace(go.Candlestick(
                    x=pd.to_datetime(df['openTime']/1000, unit='s'),
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']
        ), row=1, col =1)

    def plotNQQE(self):
        data = self.lineSeriesData
        for column in data :
            if column == 'openTime':
                continue
            else:
                self.fig.add_trace(go.Scatter(
                    x=pd.to_datetime(data['openTime']/1000, unit='s'), 
                    y=data[column], name=column
                ), row=2, col =1)

    def plotBars(self):
        data = self.lineSeriesData
        self.fig.add_trace(go.Bar(
            x=pd.to_datetime(data['openTime']/1000, unit='s'), 
            y=data['QQES']
        ), row=2, col =1)

    def plotOrders(self):
        buySeries = self.long['entry']
        sellSeries = self.long['exit']
        openTimeSeries = self.mainData['openTime']
        
        buyDF = pd.DataFrame({
            'openTime': openTimeSeries,
            'buy': buySeries
        })
        sellDF = pd.DataFrame({
            'openTime': openTimeSeries,
            'sell': sellSeries
        })

        buyDF = buyDF[buyDF['buy'] == True]
        sellDF = sellDF[sellDF['sell'] == True]

        buyDF['openTime'] = pd.to_datetime(buyDF['openTime']/1000, unit='s')
        sellDF['openTime'] = pd.to_datetime(sellDF['openTime']/1000, unit='s')

        buyTime = buyDF['openTime'].to_numpy()
        sellTime = sellDF['openTime'].to_numpy()

        # print(buyTime)

        plt.plotBuy(buyTime)
        plt.plotSell(sellTime)

        del(buyDF, sellDF, buyTime, sellTime)


    def showPlot(self, file="strategies/nQQE_plot.html"):

        self.fig.update_traces(xaxis='x')
        self.fig.write_html(file)


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


    obj = nqqeStrat(df)
    obj.initNumPy()
    
    # obj.defineOrder('QQEF < QQES', 'QQEF > s_QQEF and QQEF < -10', longFlag=False)
    obj.defineOrder('QQEF > 10 and QQEF < s_QQEF', 'QQEF > s_QQEF',longFlag=False)
    obj.plotCandles()
    obj.plotNQQE()
    obj.plotBars()
    df = obj.getOrderList()
    print(obj.portfolio)

    df.to_csv('strategies/nqqe_orders.csv')
    obj.showPlot()