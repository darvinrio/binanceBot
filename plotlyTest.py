import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import getData
from indis.hccp import getHCCP

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
# df = (pd.read_csv('test/testData.csv')).drop('Unnamed: 0',axis=1)

candles = getData.getCandles()
df = pd.DataFrame(candles)
df = df.drop([7,8,9,10,11], axis=1)
df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']

for column in df:
    if column == 'openTime' or column == 'closeTime' :
        continue
    df[column] = pd.to_numeric(df[column], downcast="float")   

print(df)

fig = go.Figure(data=[go.Candlestick(
                x=pd.to_datetime(df['openTime']/1000, unit='s'),
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

hccpData = getHCCP(df)

hccpData = hccpData.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'],axis=1)
 
for column in hccpData :
    if column == 'openTime':
        continue
    else:
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df['openTime']/1000, unit='s'), 
            y=hccpData[column]))


# fig.write_html("plot.html")
# fig.show()
fig.write_image("output/hccpPlot.png")
# print(hccpData)
