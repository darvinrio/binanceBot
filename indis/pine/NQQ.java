// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © KivancOzbilgic

//@version=4
study(" Normalized Quantitative Qualitative Estimation", shorttitle="nQQE",precision=4, resolution="")

src=input(close)
length = input(14,"RSI Length", minval=1)
SSF=input(5, "SF RSI SMoothing Factor", minval=1)
showsignals = input(title="Show Crossing Signals?", type=input.bool, defval=false)

//=======================================================================

RSII=ema(rsi(src,length),SSF)
TR=abs(RSII-RSII[1])
wwalpha = 1/ length
WWMA = 0.0
WWMA := wwalpha*TR + (1-wwalpha)*nz(WWMA[1])
ATRRSI=0.0
ATRRSI := wwalpha*WWMA + (1-wwalpha)*nz(ATRRSI[1])
QQEF=ema(rsi(src,length),SSF)
QUP=QQEF+ATRRSI*4.236
QDN=QQEF-ATRRSI*4.236
QQES=0.0
QQES:=QUP<nz(QQES[1]) ? QUP : QQEF>nz(QQES[1]) and QQEF[1]<nz(QQES[1]) ? QDN :  QDN>nz(QQES[1]) ? QDN : QQEF<nz(QQES[1]) and QQEF[1]>nz(QQES[1]) ? QUP : nz(QQES[1])
Colorh = QQEF-50>10 ? #007002 : QQEF-50<-10 ? color.red : #E8E81A

//==========================================================================

QQF=plot(QQEF-50,"FAST",color=color.maroon,linewidth=2)
plot(QQEF-50,color=Colorh,linewidth=2,style=5)
QQS=plot(QQES-50,"SLOW",color=#0007E1, linewidth=2)
hline(10,color=color.gray,linestyle=2)
hline(-10,color=color.gray,linestyle=2)
buySignalr = crossover(QQEF, QQES)
plotshape(buySignalr and showsignals ? (QQES-50)*0.995 : na, title="Buy", text="Buy", location=location.absolute, style=shape.labelup, size=size.tiny, color=color.green, textcolor=color.white, transp=0)
sellSignallr = crossunder(QQEF, QQES)
plotshape(sellSignallr and showsignals ? (QQES-50)*1.005 : na, title="Sell", text="Sell", location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.red, textcolor=color.white, transp=0)
alertcondition(cross(QQEF, QQES), title="Cross Alert", message="QQE Crossing Signal!")
alertcondition(crossover(QQEF, QQES), title="Crossover Alarm", message="QQE BUY SIGNAL!")
alertcondition(crossunder(QQEF, QQES), title="Crossunder Alarm", message="QQE SELL SIGNAL!")
alertcondition(crossover(QQEF, 50), title="Cross 0 Up Alert", message="QQE FAST Crossing 0 UP!")
alertcondition(crossunder(QQEF, 50), title="Cross 0 Down Alert", message="QQE FAST Crossing 0 DOWN!")
alertcondition(crossover(QQEF, 60), title="Cross 10 Up Alert", message="QQE Above 10 UPTREND SIGNAL!")
alertcondition(crossunder(QQEF, 40), title="Cross -10 Down Alert", message="QQE Below -10 DOWNTREND SIGNAL!")
alertcondition(crossunder(QQEF, 60) or crossover(QQEF, 40), title="SIDEWAYS", message="QQE Entering Sideways Market!")
