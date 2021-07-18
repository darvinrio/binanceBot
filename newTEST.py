from binanceAPI import dAPI
import private.keys as KEYS
from indis.hccp import getHCCP

import pandas as pd
import copy
import websocket
import websockets
import asyncio
import json
import time

api = dAPI(KEYS.botApi, KEYS.botSec)

class liveTest:
    
    def __getHistKlines(self):
        params = {
            'pair' : 'BTCUSD',
            'contractType' : 'PERPETUAL',
            'interval' : '1m',
            'limit' : 21 
        }
        klines = self.api.send_public_request('/dapi/v1/continuousKlines', params)
        return klines


    def __init__(self, KEY, SECRET):
        self.api = dAPI(KEY, SECRET)

        candlesList = self.__getHistKlines()

        self.candles = pd.DataFrame(candlesList)
        self.candles = self.candles.drop([7,8,9,10,11], axis=1)
        self.candles.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']

        for column in self.candles:
            if column == 'openTime' or column == 'closeTime' :
                continue
            self.candles[column] = pd.to_numeric(self.candles[column], downcast="float")

        self.candles = self.candles.drop([20])

        self.mainData = getHCCP(copy.deepcopy(self.candles))
        
        # self.mainData.to_csv('mainLive.csv')
        
        self.inOrder = False
        self.longOrder = True
        self.noOfOrders = 0


    async def on_message(self, message):
        json_msg = json.loads(message)
        reqMsg = json_msg['k']
        candle = {}
        action = None

        output = {}
        output['vals'] = None
        output['order'] = None

        if reqMsg['x']:
        
            candle['openTime'] = [reqMsg['t']]
            candle['open'] = [reqMsg['o']]
            candle['high'] = [reqMsg['h']]
            candle['low'] = [reqMsg['l']]
            candle['close'] = [reqMsg['c']]
            candle['volume'] = [reqMsg['v']]
            candle['closeTime'] = [reqMsg['T']]
            
            tDF = pd.DataFrame.from_dict(candle)
            for column in tDF:
                if column == 'openTime' or column == 'closeTime' :
                    continue
                tDF[column] = pd.to_numeric(tDF[column], downcast="float")

            self.candles = self.candles.drop([0])
            self.candles = self.candles.append(tDF).reset_index(drop=True)

            row = 19
            hccp = getHCCP(copy.deepcopy(self.candles))

            # hccp.to_csv('hccpLive.csv')


            openC = hccp['open'][row]
            close = hccp['close'][row]
            high = hccp['high'][row]
            low = hccp['low'][row]


            mcb = hccp['mcb'][row]
            mct = hccp['mct'][row]
            scb = hccp['scb'][row]
            sct = hccp['sct'][row]

            output['vals'] = {
                "openTime" : reqMsg['t'],
                "open" : openC,
                "high" : high,
                "low" : low,
                "close": close,
                "zhccp" :{                    
                    "mct" : mct,
                    "mcb" : mcb,
                    "sct" : sct,
                    "scb" : scb,
                }
            }

            if not(self.inOrder) and (openC <= mcb) and (close >= mcb):
                action = "LONG at" + str(high)
                self.inOrder = True
                self.longOrder = True 
                self.noOfOrders += 1

            if not(self.inOrder) and (openC >= mct) and (close <= mct):
                action = "SHORT at" + str(low)
                self.inOrder = True 
                self.longOrder = False 
                self.noOfOrders += 1

            if self.inOrder and self.longOrder and (high >= sct) :
                print("Exit Long"+ str(low))
                action = "Exit LONG at" + str(candle['low'])
                self.inOrder = False

            if self.inOrder and not(self.longOrder) and (low <= scb):
                print("ExitShort"+ str(high))
                action = "Exit SHORT at" + str(high)
                self.inOrder = False
        
            output['inOrder'] = self.inOrder
            output['no of Orders'] = self.noOfOrders
            output['action'] = action
            print(output)
        
        else :
            print('boop')   


    async def runSocket(self):
        socketURL = 'wss://dstream.binance.com/ws/btcusd_perpetual@continuousKline_1m'
        # self.ws = websocket.WebSocketApp(socketURL,on_open=self.on_open, on_message=self.on_message)

        # self.ws.run_forever()

        while True:
            try:
                async with websockets.connect(socketURL) as ws:
                    while True:
                        asyncio.create_task(self.on_message(await ws.recv()))
            except Exception as e:
                print(e)


    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.runSocket())
        loop.close() 

if __name__ == "__main__":
    obj = liveTest(KEYS.botApi, KEYS.botSec)
    obj.run()
        

