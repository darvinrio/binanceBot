import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from plotly.subplots import make_subplots

from indis.hccp import getHCCP

# df = (pd.read_csv('test/testData.csv')).drop('Unnamed: 0',axis=1)
fig = go.Figure()
fig.update_layout(hovermode="x")
fig.update_yaxes(fixedrange=False)

def initSubPlots(r, c):
    """
        r - rows
        c - columns
    """
    global fig
    fig = make_subplots(rows=r, cols=c, shared_xaxes=True)

def plotCandles(df, r=1, c=1):
    fig.add_trace(go.Candlestick(
                x=pd.to_datetime(df['openTime']/1000, unit='s'),
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
    ), row=r, col =c)

def plotLines(data, r=1, c=1):
    for column in data :
        if column == 'openTime':
            continue
        else:
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(data['openTime']/1000, unit='s'), 
                y=data[column], name=column
            ), row=r, col =c)

def plotBuy(dates,r=1, c=1):
    for date in dates:
        fig.add_vline(
            x = str(date),
            line_color="green"
        )
    
def plotSell(dates,r=1, c=1):
    for date in dates:
        fig.add_vline(
            x = str(date),
            line_color="red"
        )

def showPlot(file="output/plot.html") :
    try:
        # fig.write_html(file)
        fig.show()
    except:
        print('its okay')

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

    hccpData = getHCCP(df)

    hccpData = hccpData.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'], axis=1)

    initSubPlots(1,1)

    plotCandles(df)
    plotLines(hccpData)
    showPlot()

 