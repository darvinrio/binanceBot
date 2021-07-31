from backtest import bt
from plotter import plotlyPlotter as pt 

import pandas as pd 

class momentsStrat(bt):
    
    def __init__(self, candles, portfolio=10):

        super().__init__(candles, portfolio)

        from indis.normalDist import moments 

        self.momentsData = moments(self.candles)

        
    def plotCandles(self):

        self.figure = pt(rows=2, columns=1)
        self.figure.addCandles(self.candles)


    def plotLineSeries(self):

        self.figure.addLineSeries(
            self.momentsData.drop(['logReturn'], axis=1),
            row=2,
            column=1
        )


    def plotBarSeries(self):

        from indis.normalDist import getMeanColorData
        barColor = getMeanColorData(self.momentsData['logReturn'])
        self.figure.addBarSeries(
            self.momentsData.drop([
                'meanLogReturn',
                'upperBound',
                'lowerBound'
            ], axis=1),
            row=2,
            column=1,
            colorSeries=barColor
        )

    
    def savePlot(self, file="strategies/moments/plot.html"):
    
        self.figure.savePlot(file)


    def showPlot(self):

        self.figure.showPlot()


    def plotALL(self):

        self.plotCandles()
        self.plotLineSeries()
        self.plotBarSeries()


    def runTest(self):

        self.initNumPy()

if __name__ == "__main__":
    
    import getData
    candles = getData.getCandles(
        symbol="BTCUSDT", 
        leng='1 week', 
        time=30, 
        klineType="FUTURES"
    )
    df = pd.DataFrame(candles)
    df = df.drop([7,8,9,10,11], axis=1)
    df.columns = ['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime']

    for column in df:
        if column == 'openTime' or column == 'closeTime' :
            continue
        df[column] = pd.to_numeric(df[column], downcast="float")   

    # print(df)

    obj = momentsStrat(df)

    # print(obj.candles)
    obj.plotALL()
    obj.savePlot()