import pandas as pd
import plotlyTest as plt
import numpy as np
import getData
import copy
#tohlct
class bt:
    """
        By default: \n
        Long is from candle.high to candle.low \n
        Short is from candle.low to candle.high \n
    """
    

    order = {
        "type" : None,
        "order": {
            "coinAmt" : 0,
            "usdtAmt" : 0,
            "enterPrice" : 0,
            "exitPrice" : 0,
            "entryTime" : "",
            "exitTime" : "" 
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
        self.orderList = []

        for column in self.candles:
            if column == 'openTime' or column == 'closeTime' :
                continue
            self.candles[column] = pd.to_numeric(self.candles[column], downcast="float")
            self.mainData[column] = pd.to_numeric(self.mainData[column], downcast="float")

        # plt.plotCandles(self.candles)

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
        self.mainData.dropna().reset_index(drop=True)


    def defineOrder(self, entryCondition, exitCondition, longFlag = True): 
        # condition = 'open < mcb and close > mcb'
        """
            orderType = 'long' or 'short'
        """
        if longFlag :
            orderType = 'long'
            orderFlag = 1
        else :
            orderType = 'short'
            orderFlag = -1 

        entryCondition = self.__parseCondition(entryCondition)
        exitCondition = self.__parseCondition(exitCondition)
        
        for column in range(self.npColumn):
            if self.order["type"] is None and eval(entryCondition):

                if longFlag:
                    entryPrice = self.dataNP[2][column]
                else :
                    entryPrice = self.dataNP[3][column]

                self.order['type'] = orderType
                self.order['order']['coinAmt'] = (self.portfolio*self.leverage)/entryPrice
                self.order['order']['usdtAmt'] = self.portfolio
                self.order['order']['enterPrice'] = entryPrice
                self.order['order']['entryTime'] = self.dataNP[0][column]

                self.long.iloc[column,0] = True

            if self.order["type"] is not(None) and eval(exitCondition):

                if longFlag:
                    exitPrice = self.dataNP[3][column]
                else :
                    exitPrice = self.dataNP[2][column]

                self.order['order']['exitPrice'] = exitPrice
                self.order['order']['exitTime'] = self.dataNP[0][column]

                coinsAmt = self.order['order']['coinAmt']
                entryPrice = self.order['order']['enterPrice']
                self.portfolio = orderFlag * ((coinsAmt * exitPrice) - (self.order['order']['usdtAmt'] * self.leverage)) + self.order['order']['usdtAmt']
                profit = self.portfolio - self.order['order']['usdtAmt']
                coinChange = exitPrice - self.order['order']['enterPrice']

                currentOrder = copy.deepcopy(self.order)
                currentOrder['profit'] = profit
                currentOrder['profitPercent'] = profit * 100 / self.order['order']['usdtAmt']
                currentOrder['coinChange'] = coinChange

                self.orderList.append(currentOrder)
                del(currentOrder)

                self.order['type'] = None
                self.order['order']['coinAmt'] = 0
                self.order['order']['usdtAmt'] = self.portfolio
                self.order['order']['enterPrice'] = 0
                self.order['order']['exitPrice'] = 0
                self.order['order']['entryTime'] = ""
                self.order['order']['exitTime'] = ""

                self.long.iloc[column,1] = True


    def printCandles(self):
        """
            plots candles using plotly.py
        """
        print(self.candles)


    def getOrderList(self):
        """
            Returns list of orders in pandas Dataframe
        """  
        return pd.json_normalize(self.orderList)


    def plotCandles(self):             
        plt.plotCandles(self.candles)


    def plotLineSeries(self):
        plt.plotLines(self.lineSeriesData)


    def plotOrders(self):
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

        del(buyDF, sellDF, buyTime, sellTime)


    def showPlot(self):
        plt.showPlot()



if __name__ == "__main__":

    candles = getData.getCandles(leng='1 day', time=1)
    df = pd.DataFrame(candles)
    df = df.drop([7,8,9,10,11], axis=1)
    df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']

    from indis.hccp import getHCCP
    class strategy(bt):        
        def __init__(self, candles, portfolio=0):

            super().__init__(candles, portfolio)
            self.hccp = getHCCP(self.candles)

            self.setLineSeriesData(self.hccp.drop(['open', 'high', 'low', 'close', 'volume', 'closeTime'], axis=1))

        def plotHccp(self):
            self.plotLineSeries()

    strat = strategy(df,10)
    strat.initNumPy()
    strat.defineOrder('open < mcb and close > mcb', 'high > sct')
    strat.defineOrder('open > mct and close < mct', 'low < scb', longFlag=False)
    
    df = strat.getOrderList()
    print(strat.portfolio)
    df.to_csv('orders.csv')
