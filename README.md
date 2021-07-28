# binanceBot
simple trading bot with flask backend and html+js ui (currently no UI though)

## progress
* So far managed to download and plot the Binance BTCUSDT 1min data 
* Calculate HCCP for the data and plot it too
* Testing HCCP showed significant repaint that rendered live data useless

* Now working on a indicator based on standard deviation of logreturns (madb)
* Works fine during sideways market
* Takes losses during massive bull and bear moves


Current interactive output for is available in output folder `strategies/madb/plot.html`

Create a `private` folder and copy `keys.py` from `keysTemplate` folder and add your binance API keys
Run the app using `flask` to run `app.py` or running `plotlyTest.py`
