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

    flag = False # flag for inOrder

    for column in range(c):
        if not(flag) and ((dNP[3][column] >= dNP[8][column]) and (dNP[8][column] >= dNP[0][column])) :
            print('enter at ' + str(dNP[1][column]))
            flag = True
            buy[column] = True

        if flag and (dNP[1][column] >= dNP[5][column]) :
            print('exit at ' + str(dNP[2][column]))
            flag = False
            sell[column] = True
        

    b = pd.DataFrame({'buy': buy})
    s = pd.DataFrame({'sell': sell})

    result = pd.concat([hccpData, b, s], axis=1, join="inner")

    print(result)

    buy = result[result['buy'] == True]
    sell = result[result['sell'] == True]

    buy['openTime'] = pd.to_datetime(buy['openTime']/1000, unit='s')
    buyTime = buy['openTime'].to_numpy()

    sell['openTime'] = pd.to_datetime(sell['openTime']/1000, unit='s')
    sellTime = sell['openTime'].to_numpy()

    data = hccpData.drop(['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime'], axis=1)
    plt.plotCandles(result, data)

    plt.plotBuy(buyTime)
    plt.plotSell(sellTime)

    plt.showPlot()