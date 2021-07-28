import private.keys as KEYS
from binance.client import Client
import pandas as pd
from binance.enums import HistoricalKlinesType
from binance.client import Client
client = Client(KEYS.key,KEYS.secret)

def getCandles(symbol="BTCUSDT", leng = '1 day', time = '1', klineType = 'SPOT'):
    """
        time in minutes only \n
        klineType : {SPOT, FUTURES}
    """
    timeStr = "Client.KLINE_INTERVAL_"+str(time)+"MINUTE"
    klineStr = "HistoricalKlinesType."+klineType

    candles = client.get_historical_klines(
        symbol,
        eval(timeStr), 
        leng + " ago UTC",
        klines_type=eval(klineStr)
    )
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
    df.to_csv('test/testData.csv')


