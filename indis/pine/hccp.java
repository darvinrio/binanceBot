//
// @author LazyBear 
// List of all my indicators: http://bit.ly/1LQaPK8
// 
study("Hurst Cycle Channel Clone [LazyBear]", shorttitle="HCCC_LB", overlay=true)
scl_t =  input(10, title="Short Cycle Length?")
mcl_t =  input(30, title="Medium Cycle Length?")
scm =  input(1.0, title="Short Cycle Multiplier?")
mcm =  input(3.0, title="Medium Cycle Multiplier?")
src=input(close, title="Source")
scl = scl_t/2, mcl = mcl_t/2
ma_scl=rma(src,scl)
ma_mcl=rma(src,mcl)
////////////////////////////
scm_off = scm*atr(scl)
mcm_off = mcm*atr(mcl)
scl_2=scl/2, mcl_2=mcl/2
//////////////////////////
sct =  nz(ma_scl[scl_2], src)+ scm_off
scb =  nz(ma_scl[scl_2], src)- scm_off
mct =  nz(ma_mcl[mcl_2], src)+ mcm_off
mcb =  nz(ma_mcl[mcl_2], src)- mcm_off
scc=#E8E8E8, mcc=#E8E8E8 
sccm=gray, mccm=black
sccf=red, mccf=green
sctl=plot(sct, color=scc, title="ShortCycleTop")
scbl=plot(scb, color=scc, title="ShortCycleBottom")
plot(avg(sct,scb), title="ShortCycleMedian", color=sccm, style=line)
mctl=plot(mct, color=mcc, title="MediumCycleTop", style=line, linewidth=0)
mcbl=plot(mcb, color=mcc, title="MediumCycleBottom", style=line, linewidth=0)
plot(avg(mct,mcb), title="MediumCycleMedian", color=mccm, style=line)
fill(sctl, scbl, sccf)
fill(mctl, mcbl, mccf)


// plotshape(r==r[1], location=location.top, style=shape.square,  color=color.blue, transp=70)
plotshape(close>mcb and open<mcb, location=location.bottom, style=shape.triangleup, color=#00FF00ff, transp=70)
plotshape(close<mct and open>mct, location=location.top, style=shape.triangledown,  color=#FF0000ff, transp=70)

alertcondition((close>mct) or (close<mcb) , title="HCCP cross", message="HCCP outside medium bands")


