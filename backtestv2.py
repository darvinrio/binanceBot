import pandas as pd
import numpy as np 
import copy

class backtest:
    """
        Entry from current close +/- input percent (market order sim) \n
        Use high/low to calculate stop exits \n        
    """
    order = {
        "type": None,
        "entry": 0,
        "exit": 0,
        "entryTime" : 0,
        "exitTime": 0
    }
    dataColumns = {}
    i=0


    def __columnCtrl(self):
        for column in self.mainData:
            try:
                tmp = self.dataColumns[column]
                del(tmp)
            except:
                self.dataColumns[column] = self.i 
                self.i += 1


    def parseCondition(self, condition):
        self.__columnCtrl()
        try:
            arr = condition.split()
        except AttributeError:
            return condition
        for i in range(len(arr)):
            try:
                tmp = str(self.dataColumns[arr[i]])
                arr[i] = "row['" + arr[i] + "']"
            except KeyError:
                continue
        return ' '.join(arr)


    def __genSig(self, row):
        print(eval(self.orderCondition['longEntry']))


    def __init__(self, candles, marketEntryPercent=0, marketExitPercent=0, stopLoss=0):

        self.candles = candles
        self.marketEntry = marketEntryPercent
        self.marketExit = marketExitPercent
        self.stopLoss = stopLoss 

        # PREPPING DATA
        # float conversion
        for column in self.candles:
            if column == 'openTime':
                continue
            self.candles[column] = pd.to_numeric(self.candles[column], downcast="float")
        # date conversion
        self.candles['openTime']=pd.to_datetime(self.candles['openTime']/1000, unit='s')

        self.mainData = copy.deepcopy(self.candles)

        
    def addData(self, data):
        try:
            self.mainData = pd.concat([self.mainData, data.drop(['openTime'], axis=1)], axis=1)
        except KeyError:
            self.mainData = pd.concat([self.mainData, data], axis=1)


    def setEntryExit(self, orderCondition):
        """
            Enter order Conditions in the below format
            orderCondition = {
                'longEntry': None,
                'longExit': None,
                'shortEntry': None,
                'shortExit': None
            }
        """
        self.orderCondition = orderCondition
        for condition in self.orderCondition:
            self.orderCondition[condition] = self.parseCondition(self.orderCondition[condition])

    def generateSignals(self):
        self.mainData['longEntry'] = False
        self.mainData['longExit'] = False
        self.mainData['shortEntry'] = False
        self.mainData['shortExit'] = False
        self.Signals = self.mainData[['longEntry', 'longExit', 'shortEntry', 'shortExit']]
        self.mainData = self.mainData.drop(['longEntry', 'longExit', 'shortEntry', 'shortExit'], axis=1)
        self.mainData.apply(self.__genSig, axis=1)


if __name__ == "__main__":
    df = pd.read_csv('test/testData.csv').drop(['Unnamed: 0','closeTime'], axis=1) 
    obj = backtest(df)

    from indis.panda_hccp import HCCP
    hccp = HCCP(obj.candles)
    obj.addData(hccp)

    conditions = {
                'longEntry': 'open > close or close > open',
                'longExit': None,
                'shortEntry': None,
                'shortExit': None
            }
    obj.setEntryExit(conditions)


    obj.generateSignals()
    print(obj.mainData)
    # print(obj.parseCondition('open > close'))
