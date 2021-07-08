from flask import Flask, render_template, jsonify
import getData 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    candles = getData.getCandles()
    newCandles = []
    for candle in candles :
        newCandle = { 
            'time' : candle[6], 
            'open' : candle[1], 
            'high' : candle[2], 
            'low' : candle[3], 
            'close' : candle[4] 
            }
        newCandles.append(newCandle)

    return jsonify(newCandles)