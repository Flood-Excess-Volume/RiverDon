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
from pandas import read_excel
import bisect
import numpy as np
from array import *
from pandas import datetime
import calendar

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
# nlength  = length of array used when nriverflag = 1
ncheck = 1 #  Superfluous test/check figures ; set ncheck=0 to remove
(nriver,nratingc,nriverflag,nlength) = (10,1,0,0)
(nriver,nratingc,nriverflag,nlength) = (13,1,10,1000)
(nriver,nratingc,nriverflag,nlength) = (13,1,370,100)
(nriver,nratingc,nriverflag,nlength) = (13,1,375,30)
 # (nriver,nratingc,nriverflag,nlength) = (13,1,0,0)
#
if nriver == 1: # River Don Rotherham/Tesco 24-10-2019 to 13-11-2019 ; (nriver,nractingc,nriverflag)=(1 0 0 0)
    Data = pd.read_csv('DonTesco201911.csv') # Suboptimal: not the source file from EA but editted file; needs to be source file
    # Full data file: RotherhamTesco_F0600_15minFlow_241019_131119.csv and RotherhamTesco_F0600_15minStage_241019_131119.csv
    ht = 1.9 # Threshold
    error = 0.08  # upper bounds chosen
    stitle = 'River Don at Rotherham/Tesco 2019'
    # 
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
elif nriver == 10: # River Ciliwung updated by Onno 01-017-2021 ; (nriver,nractingc,nriverflag)=(10 1 0 0) Nico Septianus' case
    # Full data source file: error see Septianus' thesis
    # Data = pd.read_excel(xlsx_file,sheetname='ciliwungdata.xlsx')
    # Data = pd.read_excel(r'ciliwungdata.xlsx', engine='openpyxl') #  Works
    Data = pd.read_excel('ciliwungdata.xlsx')
    # Data = pd.read_csv('ciliwungdata.csv') #  Works
    ht = 2.8
    error = 0.05
    stitle = 'River Ciliwung flood 2020 at Depok floodgate, Djakarta'
    # Different from River Ciliwung case in excel file parameters.xlsx with parameters (a<->b coefficients interchanged?)
    # Note that Q(h) = c_j*(h-a_j)**b_j
    c = [11.403]
    a = [0.2]
    b = [1.715]
    Qt = c[0]*(ht-a[0])**(b[0]) # Q(ht) should work TODO
    # Upper and lower limits of ranges of river heights given for rating curve.
    lower_limits = [0.0]
    upper_limits = [10]
    print(' nriver=10: Ciliwung river, cut-off not precise')

elif nriver == 11: # New river ; (nriver,nractingc,nriverflag)=(11 0 0)
    # Full data source file:
    # Data = pd.read_csv('TBD.csv')
    # ht = TBD
    # error = TBD
    stitle = 'River TBD at TBD'
    print(' nriver=11: working.')

elif nriver == 12: # River Ouse flood 2015; (nriver,nractingc,nriverflag)=(12 0 0 0) Antonia Feilden's 2018 project case 2015 York, 2000? York?
    # Full data source file:
    Data = pd.read_csv('skelton 2015.csv')
    ht = 6.17
    error = 0.08
    stitle = 'River Ouse flood 2015 at Skelton in York'
    print(' nriver=13: working but standard case does not apply given the hysteresis.')

elif nriver == 13: # River Tamar in Devon; (nriver,nratingc,nriverflag,nlength) = (13,1,370,100) Onno's Matlab case 2018
    # Full data source file: now hourly data
    Data = pd.read_csv('river-tamar-gulworthy-gunnislake.csv')
    ht = 2.95
    error = 0.08
    lower_limits = [0.1890, 0.3650]
    upper_limits = [0.3650, 3.9840]
    c = [30.4515824141758, 31.4420090976431]
    b = [3.89481846477192, 1.99812525109993]
    a = [-0.237667493077846, -0.00174326407201127]
    stitle = 'River Tamar flood 2013 at Gunnislake'
    print(' nriver=13: not yet working TBD.')

#
# Read in time and height data from "Data" file and make special plots
#
if nriver == 10: # Ciliwung river case is special
    time = Data['Day']
    # Flow = Data['Flowrate'] # Fails to read in; why?
    height = Data['Riverheight']
elif nriver == 12: # Ouse river case is special
    time = Data['Day']
    height = Data['Stage']
    Flow = Data['Flow'] # Specific for case where flow data given as well instead of rating curve; reprogram
elif nriver == 13: # Tamar river case is special
    datum = Data['date']
    tijd = pd.to_datetime(datum)
    yr = tijd.dt.year
    time =  tijd.dt.dayofyear
    # ts = pd.Timestamp(tijd)
    for jj in range(0,len(datum)): 
        ts = pd.Timestamp(datum[jj])
        aa = np.ceil(ts.to_julian_date())
        aa = aa.astype(int)
        time[jj] = aa

    # aa = np.ceil(ts.to_julian_date('24-12-2013'))
    # aa = aa.astype(int)
    time = time-time[0]
    time = time-nriverflag-2
    height = Data['avg_level']
    heightmin = Data['min_level']
    heightmax = Data['max_level']
else: # main case
    time = Data['Time']
    height = Data['Height']
    
    
#
# Establish flow/discharge data either from "Data" file or via rating curve
#
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
    if nriverflag > 0 and nlength == 0: # slice arrays to ignore first nriverflag number of data; clumsy slicing set up
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
        print('HALLO111 HALLO111')
        # 
        print('hallo WARNING: very clumsy way of slicing and reducing; please improve')
    elif nriverflag > 0 and nlength > 0: # slice arrays from nriverflag to nriverflag+nlength
        lent = len(time)
        time1 = np.zeros(nlength)
        height1 = np.zeros(nlength)
        Flow1 = np.zeros(nlength)
        time1[0:nlength] = time[nriverflag:nriverflag+nlength] #
        height1[0:nlength] = height[nriverflag:nriverflag+nlength]
        Flow1[0:nlength] = Flow[nriverflag:nriverflag+nlength]
        (time2, height2, Flow2) = (time, height, Flow)           
        del time, height, Flow
        time = np.zeros(nlength)
        height = np.zeros(nlength)
        Flow = np.zeros(nlength)
        time = time1
        height = height1
        Flow = Flow1
        if nriver == 13:
            heightmin1 = np.zeros(nlength)
            heightmax1 = np.zeros(nlength)
            heightmin1[0:nlength] = heightmin[nriverflag:nriverflag+nlength]
            heightmax1[0:nlength] = heightmax[nriverflag:nriverflag+nlength]   
            del heightmin, heightmax
            heightmin = np.zeros(nlength)
            heightmax = np.zeros(nlength)
            heightmin = heightmin1
            heightmax = heightmax1
        # (time, height, Flow) = (time1, height1, Flow1)
        # del time1, height1, Flow1
        # print('HALLO time same same',time,nriverflag,nlength)
elif nratingc == 0:
    if nriver == 10: # special case Ciliwung river
        Flow = Data['Flowrate'] # Specific for case where flow data given as well instead of rating curve; TODO reprogram does not work
    else:
        Flow = Data['Flow'] # Specific for case where flow data given as well instead of rating curve; reprogram
    nend = len(time)
    if nriverflag > 0 and nlength == 0: # slice arrays to ignore first nriverflag number of data; clumsy slicing set up
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
    elif nriverflag > 0 and nlength > 0: # slice arrays from nriverflag to nriverflag+nlength
        lent = len(time)
        time1 = np.zeros(nlength)
        height1 = np.zeros(nlength)
        Flow1 = np.zeros(nlength)
        time1[0:nlength] = time[nriverflag:nriverflag+nlength] #
        height1[0:nlength] = height[nriverflag:nriverflag+nlength]
        Flow1[0:nlength] = Flow[nriverflag:nriverflag+nlength]
        (time2, height2, Flow2) = (time, height, Flow)           
        del time, height, Flow
        time = np.zeros(nlength)
        height = np.zeros(nlength)
        Flow = np.zeros(nlength)
        time = time1
        height = height1
        Flow = Flow1
        if nriver == 13: #  Tamar river
            heightmin1 = np.zeros(nlength)
            heightmax1 = np.zeros(nlength)
            heightmin1[0:nlength] = heightmin[nriverflag:nriverflag+nlength]
            heightmax1[0:nlength] = heightmax[nriverflag:nriverflag+nlength]   
            del heightmin, heightmax
            heightmin = np.zeros(nlength)
            heightmax = np.zeros(nlength)
            heightmin = heightmin1
            heightmax = heightmax1
         #del time1, height1, Flow1
    else:
        if nriver == 13: #  Tamar river
            lent = len(time)
            heightmin1 = np.zeros(lent)
            heightmax1 = np.zeros(lent)
            heightmin1 = heightmin
            heightmax1 = heightmax
            del heightmin, heightmax
            heightmin = np.zeros(lent)
            heightmax = np.zeros(lent)
            heightmin = heightmin1
            heightmax = heightmax1

        
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
#               
# end of nratingc tell tale
#

    
if ncheck == 111: #  Superfluous test/check figures for sliced data ; set ncheck=0 at top to block
    plt.figure(101) 
    plt.plot(height,Flow,'-')
    plt.xlabel('$h$ (m)',fontsize=16)
    plt.ylabel('$Q(h)$ (m$^3$/s)',fontsize=16) 
    plt.figure(102) #  Superfluous test/check figure
    plt.plot(time,Flow,'-')
    plt.xlabel('$t$ (days)',fontsize=16)
    plt.ylabel('$Q(t)$ (m$^3$/s)',fontsize=16)
    
if nriver == 1: # River Don Rotherham Tesco
    ncheckk = 1
    if ncheckk == 1: #  Superfluous test/check figures for sliced data ; set ncheck=0 at top to block ; plots used
        plt.figure(111) 
        plt.plot(time,height,'-k', linewidth=2)
        plt.ylabel('$h(t)$ [m]',fontsize=16)
        plt.xlabel('$t$ [day]',fontsize=16)
        Qt = qt
        hmin = 0
        hmax = 3.5
        tmin = 0
        tmax = 13
        Qmin = 0
        Qmax = 650
        plt.plot([tmin,tmax],[ht,ht],'--k')
        plt.text(0.92*tmax, 1.05*ht, '$h_T$', size=18)
        plt.axis([tmin, tmax, hmin, hmax])
        plt.title("a) Don, Rotherham Tesco")
        plt.figure(112)
        plt.plot(time,Flow,'-k', linewidth=2)
        plt.plot([tmin,tmax],[Qt,Qt],'--k')
        plt.text(0.92*tmax, 1.05*Qt, '$Q_T$', size=18)
        plt.ylabel('$Q(t)$ [m$^3/$s]',fontsize=16)
        plt.text(6.8, 280, '$FEV$', size=18, rotation=90)
        plt.xlabel('$t$ [day]',fontsize=16)
        plt.axis([tmin, tmax, Qmin, Qmax])
        plt.title("a) Don, Rotherham Tesco")
        plt.figure(113)
        plt.plot(Flow,height,'-k', linewidth=2)
        plt.plot([0,Qt],[ht,ht],'--k')
        plt.text(0.1*Qmax, 1.05*ht, '$h_T$', size=18)
        plt.plot([Qt,Qt],[hmin,ht],'--k')
        plt.text(1.1*Qt, 0.05*ht, '$Q_T$', size=18)
        plt.plot([0,np.max(Flow)],[0,np.max(height)],'--b')
        plt.ylabel('$h$ [m]',fontsize=16)
        plt.xlabel('$Q$ [m$^3/$s]',fontsize=16)
        plt.axis([Qmin, Qmax, hmin, hmax])
        plt.title("a) Don, Rotherham Tesco")
elif nriver == 10: # Ciliwung river case is special
    ncheckk = 1
    if ncheckk == 1: #  Superfluous test/check figures for sliced data ; set ncheck=0 at top to block ; plots used
        plt.figure(111) 
        plt.plot(time,height,'-k', linewidth=2)
        plt.ylabel('$h(t)$ [m]',fontsize=16)
        plt.xlabel('$t$ [day]',fontsize=16)
        hmin = 0
        hmax = 4.5
        tmin = 1
        tmax = 2
        Qmin = 0
        Qmax = 150
        plt.plot([tmin,tmax],[ht,ht],'--k')
        plt.text(0.92*tmax, 1.05*ht, '$h_T$', size=18)
        plt.axis([tmin, tmax, hmin, hmax])
        plt.title("b) Ciliwung, Depok Floodgate")
        plt.figure(112)
        plt.plot(time,c[0]*(height-a[0])**b[0],'-k', linewidth=2)
        plt.plot([tmin,tmax],[Qt,Qt],'--k')
        plt.text(0.92*tmax, 1.05*Qt, '$Q_T$', size=18)
        plt.text(1.35, 80, '$FEV$', size=18)
        plt.ylabel('$Q(t)$ [m$^3/$s]',fontsize=16)
        plt.xlabel('$t$ [day]',fontsize=16)
        plt.axis([tmin, tmax, Qmin, Qmax])
        plt.title("b) Ciliwung, Depok Floodgate")
        plt.figure(113)
        Nhh = 50
        dhh = (hmax-a[0])/Nhh
        hh = np.zeros(Nhh+1)
        for jj in range (0,Nhh+1):
            hh[jj] = a[0]+jj*dhh
            print('jj',jj,dhh,hh[jj],c[0]*(hh[jj]-a[0])**(b[0])) # Q(hh(jj)) should work TODO
        plt.plot(c[0]*(hh-a[0])**(b[0]),hh,'-k', linewidth=2) # Q(hh) should work TODO
        plt.plot([0,Qt],[ht,ht],'--k')
        plt.text(0.1*Qmax, 1.05*ht, '$h_T$', size=18)
        plt.plot([Qt,Qt],[hmin,ht],'--k')
        plt.text(1.1*Qt, 0.05*ht, '$Q_T$', size=18)
        plt.plot([0,np.max(c[0]*(hh-a[0])**b[0])],[0,np.max(hh)],'--b') # Q(hh) should work TODO
        plt.ylabel('$h$ [m]',fontsize=16)
        plt.xlabel('$Q$ [m$^3/$s]',fontsize=16)
        plt.axis([Qmin, Qmax, hmin, hmax])
        plt.title("b) Ciliwung, Depok Floodgate")
elif nriver == 12: # Ouse river case is special
    ncheckk = 1
    for jj in range (1,len(height)):  # assuming there is only one pair of pass throughs
        if height[jj-1] < ht and height[jj] > ht:
            jup = jj
        if height[jj-1] > ht and height[jj] < ht:
            jdown = jj
    qtup = Flow[jup]  # approximation
    qtdown = Flow[jdown] # approximation
        
    if ncheckk == 1: #  Superfluous test/check figures for sliced data ; set ncheck=0 at top to block ; plots used
        plt.figure(111) 
        plt.plot(time,height,'-k', linewidth=2)
        plt.ylabel('$h(t)$ [m]',fontsize=16)
        plt.xlabel('$t$ [day]',fontsize=16)
        hmin = 0
        hmax = 8
        tmin = 0
        tmax = 6
        Qmin = 0
        Qmax = 600
        z = np.zeros(4)
        z = np.polyfit(height,Flow, 4)
        print('z',z)
        AA = np.zeros((4,4))
        ff = np.zeros(4)
        d11 = np.inner(height,height)
        d21 = np.inner(height**2,height)
        d31 = np.inner(height**3,height)
        d41 = np.inner(height**4,height)
        d22 = np.inner(height**2,height**2)
        d32 = np.inner(height**3,height**2)
        d42 = np.inner(height**4,height**2)
        d33 = np.inner(height**3,height**3)
        d43 = np.inner(height**4,height**3)
        d44 = np.inner(height**4,height**4)
        ff[0] = np.inner(Flow,height)
        ff[1] = np.inner(Flow,height**2)
        ff[2] = np.inner(Flow,height**3)
        ff[3] = np.inner(Flow,height**4)
        AA = np.array([[d11,d21,d31,d41],[d21,d22,d32,d42],[d31,d32,d33,d43],[d41,d42,d43,d44]])
        z = np.linalg.solve(AA, ff)
        Qt = z[0]*ht + z[1]*ht**2 + z[2]*ht**3 + z[3]*ht**4
        print('z',z)
        a0 = -9539.05
        a1 = 7056.26
        a2 = -1909.17
        a3 = 227.97
        a4 = -9.97
        Flowqh = 0.0*Flow
        Flowqh = z[0]*height + z[1]*height**2 + z[2]*height**3 + z[3]*height**4
        plt.plot([tmin,tmax],[ht,ht],'--k')
        plt.text(0.92*tmax, 1.05*ht, '$h_T$', size=18)
        plt.axis([tmin, tmax, hmin, hmax])
        plt.title("c) Ouse, Skelton, York")
        plt.figure(112)
        # plt.plot(time,c[0]*(height-a[0])**b[0],'-k', linewidth=2)
        plt.plot(time,Flow,'-k', linewidth=2)
        plt.plot(time,Flowqh,'--k', linewidth=2)
        plt.plot([tmin,tmax],[Qt,Qt],'--k', linewidth=1)
        plt.plot([tmin,tmax],[qtup,qtup],'--b', linewidth=2)
        plt.plot([time[jup],time[jdown]],[qtup,qtdown],'--r', linewidth=3)
        plt.plot([tmin,tmax],[qtdown,qtdown],'--b', linewidth=2)
        plt.ylabel('$Q(t)$ [m$^3/$s]',fontsize=16)
        plt.xlabel('$t$ [day]',fontsize=16)
        plt.axis([tmin, tmax, Qmin, Qmax])
        plt.title("c) Ouse, Skelton, York")
        plt.text(0.85*tmax, 1.02*Qt, '$Q_T$', size=18)
        plt.text(0.85*tmax, 1.04*qtup, '$Q_{T_{up}}$', size=18)
        plt.text(0.85*tmax, 0.92*qtdown, '$Q_{T_{down}}$', size=18)
        plt.figure(113)
        Nhh = 50
        dhh = hmax/Nhh
        hh = np.zeros(Nhh+1)
        Qq = np.zeros(Nhh+1)
        for jj in range (0,Nhh+1):
            hh[jj] = jj*dhh
            Qq[jj] = z[0]*hh[jj] + z[1]*hh[jj]**2 + z[2]*hh[jj]**3 + z[3]*hh[jj]**4
        plt.plot(Qq,hh,'--k', linewidth=2)
        plt.plot(Flow,height,'-k', linewidth=2)
        plt.plot([0,Qmax],[ht,ht],'--k')
        plt.plot([Qt,Qt],[hmin,ht],'--k')
        plt.plot([qtup,qtup],[hmin,ht],':b')
        plt.plot([qtdown,qtdown],[hmin,ht],':b')
        plt.plot([0,np.max(Flow)],[0,np.max(height)],'--b')
        plt.text(1.02*Qt, 0.05*ht, '$Q_T$', size=18)
        plt.text(1.02*qtup, 0.05*ht, '$Q_{T_{up}}$', size=18)
        plt.text(0.8*qtdown, 0.05*ht, '$Q_{T_{down}}$', size=18)
        plt.text(0.1*Qmax, 1.05*ht, '$h_T$', size=18)
        plt.ylabel('$h$ [m]',fontsize=16)
        plt.xlabel('$Q$ [m$^3/$s]',fontsize=16)
        plt.axis([Qmin, Qmax, hmin, hmax])
        plt.title("c) Ouse, Skelton, York")
elif nriver == 13: # Tamar river case is special
    ncheckk = 1
    if ncheckk == 1: #  Superfluous test/check figures for sliced data ; set ncheck=0 at top to block ; plots used
        hmin = 0
        hmax = 3.5
        tmin = 0 #  nriverflag
        tmax = nlength # nriverflag+nlength
        Qmin = 0
        Qmax = 350
        plt.figure(111)
        print('lengte',len(Flow),nlength, time, height)
        # for jj in range (1,nlength):
           # p plt.plot([time[jj],time[jj]+1],[height[jj],height[jj]],'-k', linewidth=2)
           # p plt.plot([time[jj],time[jj]+1],[heightmin[jj],heightmin[jj]],'-k', linewidth=1)
           # p plt.plot([time[jj],time[jj]+1],[heightmax[jj],heightmax[jj]],'-k', linewidth=1)
        plt.plot(time,heightmin,':k', linewidth=1)
        plt.plot(time,height,'-k', linewidth=2)
        plt.plot(time,heightmax,':k', linewidth=1)
        plt.plot([tmin,tmax],[ht,ht],'--k')
        plt.text(0.92*tmax, 1.04*ht, '$h_T$', size=18)
        plt.axis([tmin, tmax, hmin, hmax])
        plt.ylabel('$h(t)$ [m]',fontsize=16)
        # plt.xlabel('$t$ [day since 26-11-2012]',fontsize=16)
        plt.xlabel('$t$ [day]',fontsize=16)
        plt.title("d) Tamar, Gunnislake")
        plt.figure(112)
        Flowmin = np.zeros(nlength)
        Flowmax = np.zeros(nlength)
        for jj in range (1,nlength):
            Flowmin[jj] = Q(heightmin[jj])
            Flowmax[jj] = Q(heightmax[jj])
        # pfor jj in range (1,nlength):
           # p plt.plot([time[jj],time[jj]+1],[Flow[jj],Flow[jj]],'-k', linewidth=2)
        plt.plot(time,Flow,'-k', linewidth=2)
        plt.plot(time,Flowmin,':k', linewidth=1)
        plt.plot([tmin,tmax],[qt,qt],'--k')
        plt.text(0.92*tmax, 1.04*qt, '$Q_T$', size=18)
        plt.plot(time,Flowmax,':k', linewidth=1)
        plt.axis([tmin, tmax, Qmin, Qmax])
        plt.ylabel('$Q(t)$ [m$^3/$s]',fontsize=16)
        # plt.xlabel('$t$ [day since 26-11-2012]',fontsize=16)
        plt.xlabel('$t$ [day]',fontsize=16)
        plt.title("d) Tamar, Gunnislake")
        plt.figure(113) 
        plt.plot(Flow2,height2,'.k', linewidth=2)
        plt.plot([qt,qt],[hmin,ht],'--k')
        plt.plot([0,Qmax],[ht,ht],'--k')
        plt.ylabel('$h$ [m]',fontsize=16)
        plt.xlabel('$Q$ [m$^3/$s]',fontsize=16)
        plt.text(1.02*qt, 0.05*ht, '$Q_T$', size=18)
        plt.text(0.1*Qmax, 1.05*ht, '$h_T$', size=18)
        plt.axis([Qmin, Qmax, hmin, hmax])
        plt.title("d) Tamar, Gunnislake")
  

plt.savefig("test.png")

plt.show(block=True)
plt.pause(0.001)
plt.gcf().clear()
plt.show(block=False)

print("Finished program!")
