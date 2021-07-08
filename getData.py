import private.keys as KEYS
from binance.client import Client
import dask.dataframe as dd

client = Client(KEYS.key,KEYS.secret)

def getCandles():
    candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    return candles

def prepTest(file):
    df = dd.read_csv(file)
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

    prepTest('test/BTCUSDT_1day_5min.csv')
