import private.keys as KEYS
from binance.client import Client
import pandas as pd

client = Client(KEYS.key,KEYS.secret)

def getCandles():
    candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    return candles

def prepTest(file):
    df = pd.read_csv(file)
    df = df.drop(['assetVolume', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'ignore', 'ignoreAgain'], axis=1)
    print(df.head())
    df.to_csv('test/testData.csv')

if __name__ == "__main__":
    import csv    
    # candles = getCandles()
    # with open("test/BTCUSDT_1day_5min.csv", "w") as f:
    #     writer = csv.writer(f)
    #     writer.writerow([
    #         'openTime',
    #         'open',
    #         'high',
    #         'low',
    #         'close',
    #         'volume',
    #         'closeTime',
    #         'assetVolume',
    #         'Taker buy base asset volume',
    #         'Taker buy quote asset volume',
    #         'ignore',
    #         'ignoreAgain'
    #     ])
    #     writer.writerows(candles)

    # prepTest('test/BTCUSDT_1day_5min.csv')

    candles = getCandles()
    df = pd.DataFrame(candles)
    df = df.drop([7,8,9,10,11], axis=1)
    df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']
    print(df)

