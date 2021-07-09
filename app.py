from flask import Flask, render_template, jsonify
import getData 
import indis
import pandas as pd
from indis.hccp import getHCCP
import json
from jsonIndi import toJson

app = Flask(__name__)

candles = getData.getCandles()
df = pd.DataFrame(candles)
df = df.drop([7,8,9,10,11], axis=1)
df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']

for column in df:
    if column == 'openTime' or column == 'closeTime' :
        continue
    df[column] = pd.to_numeric(df[column], downcast="float")   

# sample = open('out.txt', 'w')
# print('dataHCCP', file = sample)  
# print(df, file = sample)
# sample.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    newCandles = []
    for candle in candles :
        newCandle = { 
            'time' : candle[0] / 1000, 
            'open' : candle[1], 
            'high' : candle[2], 
            'low' : candle[3], 
            'close' : candle[4] 
            }
        newCandles.append(newCandle)

    return jsonify(newCandles)

@app.route('/hccp')
def dataHCCP():
    hccpData = getHCCP(df)

    hccpData = hccpData.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'],axis=1)
    x = toJson(hccpData)

    return jsonify([x])