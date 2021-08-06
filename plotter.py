import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.subplots import make_subplots

class plotlyPlotter:

    def parseTimeStamp(self, timeSeries):

        return pd.to_datetime(timeSeries/1000, unit='s')


    def __init__(self, rows=1, columns=1): 

        self.rows = rows
        self.columns = columns       
        self.fig = make_subplots(
            rows=self.rows, 
            cols=self.columns, 
            shared_xaxes=True,
            vertical_spacing=0
        )

        self.fig.update_layout(hovermode="x")
        self.fig.update_xaxes(rangeslider_visible=False)
        self.fig.update_yaxes(fixedrange=False)

        
    def addCandles(self, candles, row=1, column=1):

        self.fig.add_trace(go.Candlestick(
                    x=self.parseTimeStamp(candles['openTime']),
                    open=candles['open'],
                    high=candles['high'],
                    low=candles['low'],
                    close=candles['close']
                ), row=row, col =column)


    def addLineSeries(self, lineSeries, row=1, column=1, colorSeries='lightblue'):

        for line in lineSeries :
            if line == 'openTime':
                continue
            else:
                self.fig.add_trace(go.Scatter(
                    x=self.parseTimeStamp(lineSeries['openTime']), 
                    y=lineSeries[line], name=line,
                    # marker_color = colorSeries
                ), row=row, col =column)


    def addBarSeries(self, barSeries, row=1, column=1, colorSeries='orange'):
        for bars in barSeries:
            if bars == 'openTime':
                continue
            else:
                self.fig.add_trace(go.Bar(
                    x = self.parseTimeStamp(barSeries['openTime']),
                    y = barSeries[bars], name=bars,
                    marker_color = colorSeries
                ), row=row, col =column)
        

    def addOrder(self, date, longFlag=True, row=1, column=1):

        color = "green"
        if not(longFlag):
            color = "red"

        self.fig.add_vline(
            x = str(date),
            line_color=color
        )


    def savePlot(self, file="output.html"):

        try:
            self.fig.write_html(file)
        except Exception as e:
            print("exception >>>> "+ e)


    def showPlot(self):

        self.fig.show()
        

if __name__ == "__main__":
    import getData
    candles = getData.getCandles()
    df = pd.DataFrame(candles)
    df = df.drop([7,8,9,10,11], axis=1)
    df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']

    for column in df:
        if column == 'openTime' or column == 'closeTime' :
            continue
        df[column] = pd.to_numeric(df[column], downcast="float")   

    print(df)

    from indis.hccp import getHCCP
    hccpData = getHCCP(df)

    hccpData = hccpData.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'], axis=1)

    plot = plotlyPlotter()

    plot.addCandles(df)
    plot.addLineSeries(hccpData)
    plot.showPlot()