from livetest import liveTest as LT 
import private.keys as KEYS
from indis.madb import madb

import json
import pandas as pd 
import copy

class madbLiveTest(LT):

    def __init__(self, KEY, SECRET):
        super().__init__(KEY, SECRET)

    async def on_message(self, message):
        json_msg = json.loads(message)
        reqMsg = json_msg['k']
        candle = {}
        action = None

        output = {}
        output['vals'] = None
        output['order'] = None
        # print(reqMsg)

        if reqMsg['x']:
        
            candle['openTime'] = [reqMsg['t']]
            candle['open'] = [float(reqMsg['o'])]
            candle['high'] = [float(reqMsg['h'])]
            candle['low'] = [float(reqMsg['l'])]
            candle['close'] = [float(reqMsg['c'])]
            candle['volume'] = [float(reqMsg['v'])]
            candle['closeTime'] = [reqMsg['T']]
            
            self.candles = self.candles.drop([0])
            self.candles = self.candles.append(
                pd.DataFrame.from_dict(candle)
            ).reset_index(drop=True)

            row = 19
            madbData = madb(copy.deepcopy(self.candles)) 
            upper1 = madbData['upper1'][row]
            lower1 = madbData['lower1'][row]
            upper2 = madbData['upper2'][row]
            lower2 = madbData['lower2'][row]

            output['vals'] = {
                "openTime" : reqMsg['t'],
                "open" : float(reqMsg['o']),
                "high" : float(reqMsg['h']),
                "low" : float(reqMsg['l']),
                "close": float(reqMsg['c']),
                "zhccp" :{                    
                    "upper1" : upper1,
                    "lower1" : lower1,
                    "upper2" : upper2,
                    "lower2" : lower2
                }
            }

            if not(self.inOrder) and (candle['open'] <= lower2) and (candle['close'] >= lower2):
                action = "LONG at" + str(candle['high'])
                self.inOrder = True
                self.longOrder = True 
                self.noOfOrders += 1

            if not(self.inOrder) and (candle['open'] >= upper2) and (candle['close'] <= upper2):
                action = "SHORT at" + str(candle['low'])
                self.inOrder = True 
                self.longOrder = False 
                self.noOfOrders += 1

            if self.inOrder and self.longOrder and (candle['high'] >= upper1) :
                print("Exit Long"+ str(candle['low']))
                action = "Exit LONG at" + str(candle['low'])
                self.inOrder = False

            if self.inOrder and not(self.longOrder) and (candle['low'] <= lower1):
                print("ExitShort"+ str(candle['high']))
                action = "Exit SHORT at" + str(candle['high'])
                self.inOrder = False
        
            output['inOrder'] = self.inOrder
            output['no of Orders'] = self.noOfOrders
            output['action'] = action
            print(output)

        else :
            print('boop')
            if self.inOrder :
                if self.longOrder:
                    


if __name__ == "__main__":
    obj = madbLiveTest(KEYS.botApi, KEYS.botSec)
    obj.run()
        