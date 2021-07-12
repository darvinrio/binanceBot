import pandas as pd
# from indis.hccp import getHCCP
import numpy as np
import plotlyTest as plt

if __name__ == "__main__":
    
    hccpData = (pd.read_csv('test/hccpData.csv')).drop('Unnamed: 0', axis=1)

    hccpData = hccpData.drop(range(60))
    hccpData = hccpData.reset_index(drop=True)
    # inOrder :{
    # False -> not in order
    # True -> in order
    # }
    # hccpData['inOrder'] = False

    dNP = ((hccpData.drop(['openTime','closeTime'], axis=1)).to_numpy()).transpose()


    ############### print(dataNP) 
    ############### 0-open,1-high,2-low,3-close,4-volume,5-sct,6-scb,7-mct,8-mcb

    # testing long ------
    #
    # buy if candle close above mcb
    # [close > mcb] and [open < mcb]
    #
    # sell if candle touch sct
    # [high >= sct]

    print(dNP)
    r,c = np.shape(dNP)

    buy = np.full(c, False) # array for 'buy'
    sell = np.full(c, False) # array for 'sel'

    portfolio = 10 # starting portfolio
    lev = 11 #trade leverage

    flag = False # flag for inOrder
    order = {
        "type" : "long or short",
        "order": {
            "coinAmt" : 0,
            "usdtAmt" : 0,
            "enterPrice" : 0,
            "exitPrice" : 0
        } 
    }

    # print(order['order'])
    # print(type(order))
    # exit()

    for column in range(c):
        if not(flag) and ((dNP[3][column] >= dNP[8][column]) and (dNP[8][column] >= dNP[0][column])) :
            entryPrice = dNP[1][column]

            order['type'] = 'long'
            order['order']['coinAmt'] = (portfolio*lev)/entryPrice
            order['order']['usdtAmt'] = portfolio
            order['order']['enterPrice'] = entryPrice
            order['order']['exitPrice'] = dNP[2][column]

            print('enter at ' + str(entryPrice))
            print(order)

            flag = True
            buy[column] = True

        if flag and (dNP[1][column] >= dNP[5][column]) :
            exitPrice = dNP[2][column]

            coinsAmt = order['order']['coinAmt']
            entryPrice = order['order']['enterPrice']
            portfolio = (coinsAmt * exitPrice) - (order['order']['usdtAmt'] * lev) + order['order']['usdtAmt']
            profit = portfolio - order['order']['usdtAmt']
            coinChange = exitPrice - order['order']['enterPrice']

            order['type'] = None
            order['order']['coinAmt'] = 0
            order['order']['usdtAmt'] = portfolio
            order['order']['enterPrice'] = 0
            order['order']['exitPrice'] = 0

            print('exit at ' + str(exitPrice))
            print(order)
            print('profit = ' + str(profit))
            print('change in Coin Value = ' + str(coinChange))
            print('###########################')

            flag = False
            sell[column] = True

    print('Final Portfolio' + str(portfolio))

    # exit()

    b = pd.DataFrame({'buy': buy})
    s = pd.DataFrame({'sell': sell})

    result = pd.concat([hccpData, b, s], axis=1, join="inner")

    # print(result)

    buy = result[result['buy'] == True]
    sell = result[result['sell'] == True]

    buy['openTime'] = pd.to_datetime(buy['openTime']/1000, unit='s')
    buyTime = buy['openTime'].to_numpy()

    sell['openTime'] = pd.to_datetime(sell['openTime']/1000, unit='s')
    sellTime = sell['openTime'].to_numpy()

    data = hccpData.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'], axis=1)
    plt.plotCandles(result)
    plt.plotLines(data)

    plt.plotBuy(buyTime)
    plt.plotSell(sellTime)

    plt.showPlot()