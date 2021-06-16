# 
#
"""
Created on Mon Jun 29 17:30:58 2020 author: Zheming Zhang; building on code from Abbey Chapman/Mary Saunders
Improvements by Onno Bokhove June 2021 (clean-up and allowing verious rivers to be analysed in one Python program)
See: https://github.com/Flood-Excess-Volume
"""
# Imports
import matplotlib.pyplot as plt
import pandas as pd
import bisect
import numpy as np
from array import *

# Definitions/functions used
def scale(x):
    return ((x-min(x))/(max(x)-min(x)))

def unscaletime(x):
    return (((max(time) - min(time)) * x) + min(time))

def Q(x): # Discharge Q given the water level h = x iff rating curve is given; here for EA-type rating curves
    z = 0
    while z < w[-1]:
        if x > lower_limits[z] and x <= upper_limits[z]:
            y = (c[z] * ((x - a[z]) ** b[z]))
            break
        elif x > upper_limits[z]:
            z = z + 1
    else:
        y = (c[w[-1]] * ((x - a[w[-1]]) ** b[w[-1]]))
    return (y)

#
# Data import: river height data saved into a csv file
# 
# The first column must have the heading 'Time', with time values converted into days (with the digits beyond the
# decimal point representing what the hours and seconds elapsed are in terms of a fraction of a day,
#  and the second column must have the heading 'Height'. See also:
# - https://github.com/Flood-Excess-Volume (Python: River Don)
# - https://github.com/Rivers-Project-2018/How-to-do-FEV-Analysis/blob/master/README.md)
# 
# * Input river data
# * Chosen threshold height: ht
# * overall error
#
# nriver = 4     # 2  # choice of river
# nratingc = 1   # 1  # when there is a rating curve: value is 1; when flow data are given value is 0
# nriverflag = 0 # flags whether adjustment of array is needed; 0 means no; >0 means yes plus amount
ncheck = 1 #  Superfluous test/check figures ; set ncheck=0 to remove
(nriver,nratingc,nriverflag) = (3,0,1200)
#
if nriver == 1: # River Don Rotherham/Tesco 24-10-2019 to 13-11-2019 ; (nriver,nractingc,nriverflag)=(1 0 0)
    Data = pd.read_csv('DonTesco201911.csv') # Suboptimal: not the source file from EA but editted file; needs to be source file
    # Full data file: RotherhamTesco_F0600_15minFlow_241019_131119.csv and RotherhamTesco_F0600_15minStage_241019_131119.csv
    ht = 1.9 # Threshold
    error = 0.08  # upper bounds chosen
    stitle = 'River Don at Rotherham/Tesco 2019'
elif nriver == 2: # River Aire test case 26/27-12-2015 ; (nriver,nractingc,nriverflag)=(2 1 0)
    Data = pd.read_csv('Aire15.csv')
    # Full data files: "Armley F1707 Stage 15min May 15 to Mar 16.csv" "Armley F1707 Flow 15min May 15 to Mar 16.csv"
    # 01/05/2015 00:00:00 to 30/03/2016 23:45:00
    ht = 3.9
    # Rating curve coeffecients, listed starting from lowest range of heights up until heighest range.
    # Note that Q(h) = c_j*(h-a_j)**b_j
    a = [0.156, 0.028, 0.153]
    b = [1.115, 1.462, 1.502]
    c = [30.96, 27.884, 30.127]
    # Upper and lower limits of ranges of river heights given for rating curve.
    lower_limits = [0.2, 0.685, 1.917]
    upper_limits = [0.685, 1.917, 4.17]
    error = [0.0542, 0.0344, 0.0528]
    error = 0.055 # upper bounds chosen
    stitle = 'River Aire at Leeds/Armley 2015'
elif nriver == 3: # River Don Rotherham 2007 data set too large; needs to start later in current file ; (nriver,nractingc,nriverflag)=(3 0 1200)
    Data = pd.read_csv('RotherhamDon2007.csv') # Suboptimal: not a source file from EA but an editted file; needs to besource file
    # Full data source file: Rotherham_L0601_15minStage_241019_131119.csv 24/10/2019 00:00:00 to 13/11/2019 23:45:00
    ht = 1.9
    error = 0.08 # example
    nriverflag = 1200
    stitle = 'River Don at Rotherham 2007'
    print('WARNING nriver=3: slicing done')
elif nriver == 4: # River Don 2007 Sheffield Hadfields data set too large ; (nriver,nractingc,nriverflag)=(4 1 0)
    Data = pd.read_csv('SheffieldHadfields2007.csv') # Suboptimal: not a source file from EA but an editted file; needs to be the source file
    # Full data source file: SheffieldHadfields_F0605_15minStage_010107_140820.csv and SheffieldHadfields_F0605_15minFlow_010107_140820.csv
    # 01/01/2007 00:00:00 to 14/08/2020 23:45:00
    ht = 2.9 # Note that Q(h) = c_j*(h-a_j)**b_j
    # different from River Aire case in excel file parameters.xlsx with parameters (a<->b coefficients interchanged)
    b = [1.3803, 1.2967, 1.1066]
    a = [0.3077, 0.34, -0.5767]
    c = [77.2829, 79.5656, 41.3367]
    # Upper and lower limits of ranges of river heights given for rating curve.
    lower_limits = [0.39, 0.927, 1.436]
    upper_limits = [0.927, 1.426, 3.58]
    error = 0.0799 # overall upper bounds
    stitle = 'River Don at Sheffield/Hadfields 2007'
    print('WARNING nriver=4: FEV_mac, FEV_min different; sort out role of QT_min, QT_max?')
elif nriver == 5: # River Don 2019 Sheffield Hadfields data set too large ; (nriver,nractingc,nriverflag)=(5 1 0)
    Data = pd.read_csv('SheffieldHadfields2019.csv') # Suboptimal: not a source file from EA but editted file; needs to be source file
    # Full data source file: SheffieldHadfields_F0605_15minStage_010107_140820.csv and SheffieldHadfields_F0605_15minFlow_010107_140820.csv
    # 01/01/2007 00:00:00 to 14/08/2020 23:45:00
    ht = 2.9 # Note that Q(h) = c_j*(h-a_j)**b_j
    #  different from River Aire case in excel file parameters.xlsx with parameters (a<->b coefficients interchanged)
    b = [1.3803, 1.2967, 1.1066]
    a = [0.3077, 0.34, -0.5767]
    c = [77.2829, 79.5656, 41.3367]
    # Upper and lower limits of ranges of river heights given for rating curve.
    lower_limits = [0.39, 0.927, 1.436]
    upper_limits = [0.927, 1.426, 3.58]
    error = 0.0799 # overal upper bounds
    stitle = 'River Don at Sheffield/Hadfields 2019'
    print('WARNING nriver=5: FEV_mac, FEV_min different; sort out role of QT_min, QT_max?')
elif nriver == 10: # River Cilliwung by Shunyu and Yantong TO DO week 16-06-2021 ; (nriver,nractingc,nriverflag)=(5 1 0)
    # Full data source file:
    # Data = pd.read_csv('TBD.csv')
    # ht = TBD
    # error = TBD
    stitle = 'River Cilliwung at Djakarta'
    print(' nriver=10: not yet working TBD.')

elif nriver == 11: # New river ; (nriver,nractingc,nriverflag)=(5 1 0)
    # Full data source file:
    # Data = pd.read_csv('TBD.csv')
    # ht = TBD
    # error = TBD
    stitle = 'River TBD at TBD'
    print(' nriver=11: not yet working TBD.')


# Read in time and height data from "Data" file
time = Data['Time']
height = Data['Height']

# Establish flow/discharge data either from "Data" file or via rating curve
if nratingc == 1:
    w = []
    for i in range(len(a)):
        w.append(i)

    qt = Q(ht) # For case with rating curve given and no given flow data
    qtmin = (1.0-error)*qt # Use an overall error upper bound
    qtmax = (1.0+error)*qt # Use an overall error upper bound
    #  print(qt)
    Flow = []
    Flowmin = []
    Flowmax = []
    for i in height:
        Flow.append(Q(i))
        Flowmin.append((1.0-error)*Q(i)) # Use an overall error upper bound
        Flowmax.append((1.0+error)*Q(i)) # Use an overall error upper bound

    scaledFlow = []
    for i in Flow:
        scaledFlow.append((i - min(Flow)) / (max(Flow) - min(Flow)))
elif nratingc == 0:
    Flow = Data['Flow'] # Specific for case where flow data given as well instead of rating curve; reprogram
    nend = len(time)
    if nriverflag > 0: # slice arrays
        lent = len(time)
        time1 = np.zeros(lent-nriverflag)
        height1 = np.zeros(lent-nriverflag)
        Flow1 = np.zeros(lent-nriverflag)
        time1[0:lent-nriverflag] = time[nriverflag:lent] #
        height1[0:lent-nriverflag] = height[nriverflag:lent]
        Flow1[0:lent-nriverflag] = Flow[nriverflag:lent]
        del time, height, Flow
        (time, height, Flow) = (time1, height1, Flow1)
        del time1, height1, Flow1
        # 
        print('hallo WARNING: very clumsy way of slicing and reducing; please improve')
    print('nend, nendnew',nend,len(time)) # Superfluous print for checking
        
    scaledFlow = []
    for i in Flow:
        scaledFlow.append((i - min(Flow)) / (max(Flow) - min(Flow)))
    #  scaledFlow = scale(Flow)
    Flowmin = (1.0-error)*Flow
    Flowmax = (1.0+error)*Flow
    # Find qt, qtmin, qtmax
    nwin = 0
    for i in range(1,len(height)):
        if height[i] > ht and height[i-1] < ht and nwin==0:
            qt =  Flow[i-1]+(Flow[i]-Flow[i-1])*(ht-height[i-1])/(height[i]-height[i-1])
            nwin = 1
        if height[i] < ht and height[i-1] > ht and nwin==0:
            qt =  Flow[i-1]+(Flow[i]-Flow[i-1])*(ht-height[i-1])/(height[i]-height[i-1])
            nwin = 1
    qtmin = (1.0-error)*qt
    qtmax = (1.0+error)*qt
    
    if ncheck == 1: #  Superfluous test/check figures for sliced data ; set ncheck=0 at top to block
        plt.figure(101) 
        plt.plot(height,Flow,'-')
        plt.xlabel('$h$ (m)',fontsize=16)
        plt.ylabel('$Q(h)$ (m$^3$/s)',fontsize=16) 
        plt.figure(102) #  Superfluous test/check figure
        plt.plot(time,Flow,'-')
        plt.xlabel('$t$ (days)',fontsize=16)
        plt.ylabel('$Q(t)$ (m$^3$/s)',fontsize=16) 
        
# end of nratingc tell tale

# Scalings:
time_increment=(time[1]-time[0])*24*3600
number_of_days=int((len(time)*(time[1]-time[0])))
scaledtime = scale(time)
scaledheight = scale(height)
error_height_up = [i * (1+error) for i in height]
error_height_down = [i * (1-error) for i in height]
scaledtime = scale(time)
scaledheight = scale(height)

# Figures
fig, ax = plt.subplots()
plt.rcParams["figure.figsize"] = [12, 12]
plt.rcParams['axes.edgecolor'] = 'white'
fig, ax = plt.subplots()
ax.spines['left'].set_position(('zero'))
ax.spines['bottom'].set_position(('zero'))
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')

scaledFlow_up = [i*(1+error) for i in scaledFlow]
scaledFlow_down = [i*(1-error) for i in scaledFlow]
negheight = -scaledheight
negday = -(scaledtime)

# To change the colour, change 'conrflowerblue' to another colour such as 'pink'.
ax.plot(negheight, scaledFlow, 'black', linewidth=1)
ax.plot([0, -1], [0, 1], 'blue', linestyle='--', marker='', linewidth=2)
ax.plot(scaledtime, scaledFlow, 'black', linewidth=1)
ax.plot(negheight, negday, 'black', linewidth=1)

scaledht = (ht - min(height)) / (max(height) - min(height))
scaledqt = (qt - min(Flow)) / (max(Flow) - min(Flow))

QT = []
for i in scaledFlow:
    i = scaledqt
    QT.append(i)

SF = np.array(scaledFlow)
e = np.array(QT)

ax.fill_between(scaledtime, SF, e, where=SF >= e, facecolor='blue', alpha = 0.4)
idx = np.argwhere(np.diff(np.sign(SF - e))).flatten()

f = scaledtime[idx[0]]
g = scaledtime[idx[-1]]

C = unscaletime(f)
d = unscaletime(g)

Tf = (d - C) * 24

time_increment = (time[1] - time[0]) * 24 * 3600

flow = []
for i in Flow:
    if i >= qt:
        flow.append((i - qt) * (time_increment))
flowmin = []
for i in Flowmin:
    if i >= qtmin:
        flowmin.append((i - qtmin) * (time_increment))
flowmax = []
for i in Flowmax:
    if i >= qtmax:
        flowmax.append((i - qtmax) * (time_increment))

FEV = sum(flow)
FEV_min = sum(flowmin)
FEV_max = sum(flowmax)

Tfs = Tf * (60 ** 2)

qm = (FEV / Tfs) + qt
scaledqm = (qm - min(Flow)) / (max(Flow) - min(Flow))

hm = ht # WARNING Poor fix for nriver=3
if nratingc == 1:
    hm = ((qm / c[-1])**(1 / b[-1])) + a[-1]
elif nratingc == 0:
    #  print('nriver hm',nriver,hm) # Superfluous was used for checking
    nwin = 0
    for i in range(1,len(Flow)):
        if Flow[i] > qm and Flow[i-1] < qm and nwin==0:
            hm =  height[i-1]+(height[i]-height[i-1])*(qm-Flow[i-1])/(Flow[i]-Flow[i-1])
            nwin = 1
        if Flow[i] < qm and Flow[i-1] > qm and nwin==0:
            hm =  height[i-1]+(height[i]-height[i-1])*(qm-Flow[i-1])/(Flow[i]-Flow[i-1])
            nwin = 1
    #  print('nriver hm',nriver,hm) # Superfluous was used for checking
    
scaledhm = (hm - min(height)) / (max(height) - min(height))

# print('hallo',FEV,FEV_min,FEV_max,qt,qm,ht,hm) # Superfluous was used for checking

ax.plot([-scaledht, -scaledht], [-1, scaledqt], 'black', linestyle='--', linewidth=1)
ax.plot([-scaledhm, -scaledhm], [-1, scaledqm], 'black', linestyle='--', linewidth=1)
ax.plot([-scaledht, 1], [scaledqt, scaledqt], 'black', linestyle='--', linewidth=1)
ax.plot([-scaledhm, 1], [scaledqm, scaledqm], 'black', linestyle='--', linewidth=1)

ax.plot([f, f, f], [scaledqt, scaledqm, -1/5], 'black', linestyle='--', linewidth=1)
ax.plot([g, g, g], [scaledqt, scaledqm, -1/5], 'black', linestyle='--', linewidth=1)
ax.plot([f, f], [scaledqm, scaledqt], 'black', linewidth=1.5)
ax.plot([f, g], [scaledqm, scaledqm], 'black', linewidth=1.5)
ax.plot([f, g], [scaledqt, scaledqt], 'black', linewidth=1.5)
ax.plot([g, g], [scaledqm, scaledqt], 'black', linewidth=1.5)
#  plt.annotate(s='', xy=(f - 1 / 100, -1 / 5), xytext=(g + 1 / 100, -1 / 5), arrowprops=dict(arrowstyle='<->')) #  Onno 14-06-2021 defunct

h = []
for i in np.arange(1, number_of_days + 1):
    h.append(i / number_of_days)

# If you wish to set the flow to be shown on the axis by a certain increment, change all
# appearances of 50 in lines 153 and 157 to the desired increment, e.g 25 or 100.
# Otherwise leave as is.
l = np.arange(0, max(Flow) + 50, 50)
m = bisect.bisect(l, min(Flow))

n = []
for i in np.arange(l[m], max(Flow) + 50, 50):
    n.append(int(i))

# If you wish to set the height to be shown on the axis by a certain increment, change all
# appearances of 1 in lines 163 and 167 to the desired increment, e.g 0.25 or 0.5.
# Otherwise leave as is.
o = np.arange(0, max(height) + 1, 1)
p = bisect.bisect(o, min(height))

q = []
for i in np.arange(o[p], max(height) + 1, 1):
    q.append(i)

k = []
for i in q:
    k.append(-(i - min(height)) / (max(height) - min(height)))

j = []
for i in n:
    j.append((i - min(Flow)) / (max(Flow) - min(Flow)))

ticks_x = k + h

r = []
for i in h:
    r.append(-i)

ticks_y = r + j

s = []
for i in np.arange(1, number_of_days + 1):
    s.append(i)

Ticks_x = q + s
Ticks_y = s + n

ax.set_xticks(ticks_x)
ax.set_yticks(ticks_y)
ax.set_xticklabels(Ticks_x)
ax.set_yticklabels(Ticks_y)

lists1 = sorted(zip(*[negheight, scaledFlow_down]))
negheight1, scaledFlow_down1 = list(zip(*lists1))

lists2 = sorted(zip(*[negheight, scaledFlow_up]))
negheight1, scaledFlow_up1 = list(zip(*lists2))

ax.fill_between(negheight1,scaledFlow_down1,scaledFlow_up1,color="grey", alpha = 0.3)
ax.fill_between(scaledtime,scaledFlow_up,scaledFlow_down,color="grey", alpha = 0.3)
QtU = scaledqt*(1+error)
QtD = scaledqt*(1-error)
ax.fill_between([scaledtime[idx[0]], scaledtime[idx[-1]]], QtU, QtD, color = "grey", alpha = 0.3)

ax.tick_params(axis='x', colors='black', direction='out', length=9, width=1)
ax.tick_params(axis='y', colors='black', direction='out', length=9, width=1)

plt.text(-scaledht + 0.02, -1, '$h_T$', size=15)
plt.text(-scaledhm + 0.02, -1, '$h_m$', size=15)
plt.text(1, scaledqm, '$Q_m$', size=15)
plt.text(1, scaledqt, '$Q_T$', size=15)
plt.text(((f + g) / 2) -1/50, -0.18, '$T_f$', size=15)
plt.text(0.02, 1.05,'Q $[m^3/s]$', size=15)
plt.text(0.95, -0.2,'t [day]', size=15)
plt.text(-0.18, -1.11,'t [day]', size=15)
#plt.text(0.43,0.7,'FEV', size=15)
plt.text(-1.1, 0.02, '$\overline {h}$ [m]', size=15)
plt.title(f"{stitle}")

ax.scatter(0, 0, color='white')

A = round(FEV/(10**6), 2)
B = round(Tf, 2)
C = round(ht, 2)
D = round(hm, 2)
E = round(qt, 2)
F = round(qm, 2)
Amax=round(FEV_max/(10**6),2)
Amin=round(FEV_min/(10**6),2)
Emin=round(qtmin,2)
Emax=round(qtmax,2)

plt.text(0.4, -0.325, '$FEV$ ≈ ' + str(A) + 'Mm$^3$', size=15)
plt.text(0.4, -0.4, '$T_f$ = ' + str(B) + 'hrs', size=15)
plt.text(0.4, -0.475, '$h_T$ = ' + str(C) + 'm', size=15)
plt.text(0.4, -0.55, '$h_m$ = ' + str(D) + 'm', size=15)
plt.text(0.4, -0.625, '$Q_T$ = ' + str(E) + 'm$^3$/s', size=15)
plt.text(0.4, -0.7, '$Q_m$ = ' + str(F) + 'm$^3$/s', size=15)
plt.text(0.4,-0.775,'$FEV_{max}$ ≈ '+ str(Amax) +'Mm$^3$', size=15)
plt.text(0.4,-0.85,'$FEV_{min}$ ≈ '+ str(Amin) +'Mm$^3$', size=15)
plt.text(0.4,-0.925,'$Q_{Tmax}$ = '+ str(Emax) +'m$^3$/s', size=15)
plt.text(0.4,-1.0,'$Q_{Tmin}$ = '+ str(Emin) +'m$^3$/s', size=15)

plt.savefig("test.png")

plt.show(block=True)
plt.pause(0.001)
plt.gcf().clear()
plt.show(block=False)

print("Finished program!")
