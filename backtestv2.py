import pandas as pd
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

    def __init__(self, candles, marketEntryPercent=0, marketExitPercent=0, stopLoss=0):
        self.candles = candles
        self.marketEntry = marketEntryPercent
        self.marketExit = marketExitPercent
        self.stopLoss = stopLoss 
        
    def setData(self, data):
        self.data = data

    def enterLong():
        
