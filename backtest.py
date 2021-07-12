import pandas as pd
import plotlyTest as plt
import numpy as np

class bt:
    """
        By default: \n
        Long is from candle.high to candle.low \n
        Short is from candle.low to candle.high \n
    """
    orderList = []

    order = {
        "type" : None,
        "order": {
            "coinAmt" : 0,
            "usdtAmt" : 0,
            "enterPrice" : 0,
            "exitPrice" : 0
        } 
    }

    candleColumns = {} 
    i=0
    leverage = 1

    def __columnCtrl(self, data):
        for column in data :
            try:
                tmp = self.candleColumns[column]
            except:
                self.candleColumns[column] = self.i
                self.i += 1


    def __appendMain(self, data):
        self.mainData = pd.concat([self.mainData, data.drop(['openTime'], axis=1)], axis=1, join='inner')
        self.__columnCtrl(data)


    def __parseCondition(self, condition):
        arr = condition.split()
        row = None
        for i in range(len(arr)):
            try:
                row = str(self.candleColumns[arr[i]])
                arr[i] = 'self.dataNP[' + row + '][column]'
            except:
                continue
        return ' '.join(arr)


    def __init__(self, candles, portfolio=0) :
        self.candles = candles.copy()
        self.portfolio = portfolio
        self.mainData = candles.copy()

        plt.plotCandles(self.candles)

        self.__columnCtrl(candles)

        tempDF = self.candles.copy()
        tempDF['temp'] = False
        self.long = pd.DataFrame({
            'entry': tempDF['temp'],
            'exit' : tempDF['temp']
        })
        self.short = pd.DataFrame({
            'entry': tempDF['temp'],
            'exit' : tempDF['temp']
        })
        del(tempDF)


    def initNumPy(self):
        self.dataNP = ((self.mainData).to_numpy()).transpose()
        self.npRow, self.npColumn = np.shape(self.dataNP)


    def setPortfolio(self, start, lev=1):
        self.portfolio = start
        self.leverage = lev


    def setLineSeriesData(self, data):
        """
        Pass 'openTime' and all lineSeries
        """
        self.lineSeriesData = data.copy()
        self.__appendMain(data)


    def appendLineSeriesData(self, data):
        self.lineSeriesData = pd.concat([self.lineSeriesData, data], axis=1, join='inner')
        self.__appendMain(data)


    def goLong(self, entryCondition, exitCondition): 
        # condition = 'open < mcb and close > mcb'
        """
        orderType = 'long' or 'short'
        """
        entryCondition = self.__parseCondition(entryCondition)
        exitCondition = self.__parseCondition(exitCondition)

        for column in range(self.npColumn):
            if self.order["type"] is None and eval(entryCondition):
                entryPrice = self.dataNP[2][column]

                self.order['type'] = 'long'
                self.order['order']['coinAmt'] = (self.portfolio*self.leverage)/entryPrice
                self.order['order']['usdtAmt'] = self.portfolio
                self.order['order']['enterPrice'] = entryPrice

                self.long.iloc[column,0] = True

            if self.order["type"] is not(None) and eval(exitCondition):
                exitPrice = self.dataNP[3][column]
                self.order['order']['exitPrice'] = exitPrice

                coinsAmt = self.order['order']['coinAmt']
                entryPrice = self.order['order']['enterPrice']
                self.portfolio = (coinsAmt * exitPrice) - (self.order['order']['usdtAmt'] * self.leverage) + self.order['order']['usdtAmt']
                profit = self.portfolio - self.order['order']['usdtAmt']
                coinChange = exitPrice - self.order['order']['enterPrice']

                currentOrder = self.order.copy()
                currentOrder['profit'] = profit
                currentOrder['coinChange'] = coinChange
                self.orderList = [self.orderList].append(currentOrder)

                self.order['type'] = None
                self.order['order']['coinAmt'] = 0
                self.order['order']['usdtAmt'] = self.portfolio
                self.order['order']['enterPrice'] = 0
                self.order['order']['exitPrice'] = 0

                self.long.iloc[column,1] = True


    def exitOrder(self):
        orderType = self.order['type'] 
        if orderType == 'long' :
            exitPrice = 100
        elif orderType == 'short':
            exitPrice = 100

        self.order['type'] = None

        print('yolo')


    def printCandles(self):
        print(self.candles)


    def plotLineSeries(self):
        plt.plotLines(self.lineSeriesData)


    def plotLong(self):
        buySeries = self.long['entry']
        sellSeries = self.long['exit']
        openTimeSeries = self.mainData['openTime']
        
        buyDF = pd.DataFrame({
            'openTime': openTimeSeries,
            'buy': buySeries
        })
        sellDF = pd.DataFrame({
            'openTime': openTimeSeries,
            'sell': sellSeries
        })

        buyDF = buyDF[buyDF['buy'] == True]
        sellDF = sellDF[sellDF['sell'] == True]

        buyDF['openTime'] = pd.to_datetime(buyDF['openTime']/1000, unit='s')
        sellDF['openTime'] = pd.to_datetime(sellDF['openTime']/1000, unit='s')

        buyTime = buyDF['openTime'].to_numpy()
        sellTime = sellDF['openTime'].to_numpy()

        # print(buyTime)

        plt.plotBuy(buyTime)
        plt.plotSell(sellTime)


    def showPlot(self):
        plt.showPlot()

if __name__ == "__main__":

    candleData = (pd.read_csv('test/testData.csv')).drop('Unnamed: 0', axis=1)
    
    
    from indis.hccp import getHCCP
    class strategy(bt):        
        def __init__(self, candles, portfolio=0):

            super().__init__(candles, portfolio)
            self.hccp = getHCCP(self.candles)

            self.setLineSeriesData(self.hccp.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'], axis=1))

        def plotHccp(self):
            self.plotLineSeries()

    strat = strategy(candleData,10)
    # print(strat.mainData)

    strat.plotHccp()
    # print(strat.candleColumns)
    strat.initNumPy()
    # print(strat.long)
    strat.goLong('open < mcb and close > mcb', 'high > sct')
    # print(strat.long)
    # print(strat.orderList)
    # print(strat.portfolio)
    strat.plotLong()

    strat.showPlot()
