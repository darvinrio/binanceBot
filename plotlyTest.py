import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import getData
from indis.hccp import getHCCP

# df = (pd.read_csv('test/testData.csv')).drop('Unnamed: 0',axis=1)
fig = go.Figure()
fig.update_layout(hovermode="x")
fig.update_yaxes(fixedrange=False)

def plotCandles(df, data):
    fig.add_trace(go.Candlestick(
                x=pd.to_datetime(df['openTime']/1000, unit='s'),
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
    ))

    for column in data :
        if column == 'openTime':
            continue
        else:
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(df['openTime']/1000, unit='s'), 
                y=data[column], name=column
            ))

def plotBuy(dates):
    for date in dates:
        fig.add_vline(
            x = str(date),
            line_color="green"
        )
    
def plotSell(dates):
    for date in dates:
        fig.add_vline(
            x = str(date),
            line_color="red"
        )

def showPlot() :
    try:
        fig.write_html("output/plot.html")
    except:
        print('its okay')

if __name__ == "__main__":
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

    plotCandles(df, hccpData)
    showPlot()

 