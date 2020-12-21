#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 00:55:51 2020

@author: zhmingzh
"""

##Imput your own data here:##
#Your chosen threshold height.
ht=1.9



#You do not have to change the following.
import matplotlib.pyplot as plt
import pandas as pd
fig, ax = plt.subplots()

#Import your data, your river height data must be saved into a csv file
#(we are using the file 'Aire Data.csv' but you must change what your csv file 
#is saved as) within the same folder as this code is saved. The first column must have the 
#heading 'Time', with time values converted into days (with the digits beyond the
#decimal point representing what the hours and seconds elapsed are in terms of a
#fraction of a day, more information on how to do this can be found at 
#https://github.com/Rivers-Project-2018/How-to-do-FEV-Analysis/blob/master/README.md) 
#and the second column must have the heading 'Height'.
Data=pd.read_csv('Rotherham Tesco 20071.csv')
time=Data['Time']
height=Data['Height']
flow=Data['Flow']
height1=height[height>ht]
import numpy as np
hm=np.mean(height1)
print(max(height))
print(hm)
#####You do not have to change any of the rest of the code.#####
#But if you wish to change elements such as the colour or the x and y axis
#there are instructions on how to do so.
import bisect
import numpy as np

plt.rcParams["figure.figsize"] = [11,8]
plt.rcParams['axes.edgecolor']='white'
ax.spines['left'].set_position(('zero'))
ax.spines['bottom'].set_position(('zero'))
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_color('black')

time_increment=(time[1]-time[0])*24*3600

number_of_days=int((len(time)*(time[1]-time[0])))

def scale(x):
    return ((x-min(x))/(max(x)-min(x)))
error = 0.08

error_height_up = [i * (1+error) for i in height]
error_height_down = [i * (1-error) for i in height]
scaledtime=scale(time)
scaledheight=scale(height)
scaledFlow=scale(flow)
hup=ht*(1+error)
print(hup)
qt = 256
qtmax=231.5    
qtmin=273

scaledFlow_up = [i*(1+error) for i in scaledFlow]
scaledFlow_down = [i*(1-error) for i in scaledFlow]
negheight=-scaledheight
negday=-(scaledtime)

#To change the colour, change 'conrflowerblue' to another colour such as 'pink'.
ax.plot(negheight,scaledFlow,'black',linewidth=2)
ax.plot([0,-1],[0,1],'cornflowerblue',linestyle='--',marker='',linewidth=2)
ax.plot(scaledtime, scaledFlow,'black',linewidth=2)
ax.plot(negheight, negday,'black',linewidth=2)

scaledht = (ht-min(height))/(max(height)-min(height))
scaledqt = (qt-min(flow))/(max(flow)-min(flow))

QT=[]
for i in scaledFlow:
    i = scaledqt
    QT.append(i)

SF=np.array(scaledFlow)
e=np.array(QT)
    
ax.fill_between(scaledtime,SF,e,where=SF>=e,facecolor='cornflowerblue')

idx = np.argwhere(np.diff(np.sign(SF - e))).flatten()

f=scaledtime[idx[0]]
g=scaledtime[idx[-1]]

def unscaletime(x):
    return (((max(time)-min(time))*x)+min(time))

C=unscaletime(f)
d=unscaletime(g)

Tf=(d-C)*24

time_increment=(time[1]-time[0])*24*3600

Flow = []
for i in flow:
    if i>=qt:
        Flow.append((i-qt)*(time_increment))


FEV=sum(Flow)
FEV_max=14.64
FEV_min=11.82
Tfs=Tf*(60**2)

qm=(FEV/Tfs)+qt
print(qm)
scaledqm = (qm-min(flow))/(max(flow)-min(flow))


scaledhm = (hm-min(height))/(max(height)-min(height))

ax.plot([-scaledht,-scaledht],[-1,scaledqt],'black',linestyle='--',linewidth=1)
ax.plot([-scaledhm,-scaledhm],[-1,scaledqm],'black',linestyle='--',linewidth=1)
ax.plot([-scaledht,1],[scaledqt,scaledqt],'black',linestyle='--',linewidth=1)
ax.plot([-scaledhm,1],[scaledqm,scaledqm],'black',linestyle='--',linewidth=1)

ax.plot([f,f,f],[scaledqt,scaledqm,-1/5], 'black', linestyle='--', linewidth=1)
ax.plot([g,g,g],[scaledqt,scaledqm,-1/5], 'black', linestyle='--', linewidth=1)
ax.plot([f,f],[scaledqm,scaledqt], 'black',linewidth=1.5)
ax.plot([f,g],[scaledqm,scaledqm], 'black',linewidth=1.5)
ax.plot([f,g],[scaledqt,scaledqt], 'black',linewidth=1.5)
ax.plot([g,g],[scaledqm,scaledqt], 'black',linewidth=1.5)
plt.annotate(s='', xy=(f-1/100,-1/5), xytext=(g+1/100,-1/5), arrowprops=dict(arrowstyle='<->'))

h=[]
for i in np.arange(1,number_of_days+1):
    h.append(i/number_of_days)


l=np.arange(0,max(flow)+50,50)
m=bisect.bisect(l,min(flow))

n=[]
for i in np.arange(l[m],max(flow)+50,50):
    n.append(int(i))


o=np.arange(0,max(height)+1,1)
p=bisect.bisect(o,min(height))

q=[]
for i in np.arange(o[p],max(height)+1,1):
    q.append(i)

k=[]
for i in q:
    k.append(-(i-min(height))/(max(height)-min(height))) 

j=[]
for i in n:
    j.append((i-min(flow))/(max(flow)-min(flow)))

ticks_x=k+h

r=[]
for i in h:
    r.append(-i)

ticks_y=r+j


s=[]
for i in np.arange(1,number_of_days+1):
    s.append(i)

Ticks_x=q+s
Ticks_y=s+n
    
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
ax.tick_params(axis='x',colors='black',direction='out',length=9,width=1)
ax.tick_params(axis='y',colors='black',direction='out',length=10,width=1)

plt.text(-scaledht+1/100, -1,'$h_T$', size=13)
plt.text(-scaledhm+1/100, -1,'$h_m$', size=13)
plt.text(1, scaledqm,'$Q_m$', size=13)
plt.text(1, scaledqt,'$Q_T$', size=13)
plt.text(((f+g)/2)-1/50,-0.18,'$T_f$',size=13)

plt.text(0.01, 1.05,'$Q$ [m$^3$/s]', size=13)
plt.text(0.95, -0.17,'$t$ [day]', size=13)
plt.text(0.01, -1.09,'$t$ [day]', size=13)
plt.text(-1.1, 0.02,'$\overline {h}$ [m]', size=13)

ax.scatter(0,0,color='white')

A=round(FEV/(10**6),2)
B=round(Tf,2)
C=round(ht,2)
D=round(hm,2)
E=round(qt,2)
F=round(qm,2)
Amax=round(FEV_max,2)
Amin=round(FEV_min,2)
Emin=round(qtmin,2)
Emax=round(qtmax,2)
plt.text(0.4,-0.4,'$FEV$ ≈ '+ str(A) +'Mm$^3$', size=15)
plt.text(0.4,-0.475,'$FEV_{max}$ ≈ '+ str(Amax) +'Mm$^3$', size=15)
plt.text(0.4,-0.55,'$FEV_{min}$ ≈ '+ str(Amin) +'Mm$^3$', size=15)
plt.text(0.4,-0.625,'$T_f$ = '+ str(B) +'hrs', size=15)
plt.text(0.4,-0.7,'$h_T$ = '+ str(C) +'m', size=15)
plt.text(0.4,-0.775,'$h_m$ = '+ str(D) +'m', size=15)
plt.text(0.4,-0.85,'$Q_T$ = '+ str(E) +'m$^3$/s', size=15)
plt.text(0.4,-0.925,'$Q_{Tmax}$ = '+ str(Emax) +'m$^3$/s', size=15)
plt.text(0.4,-1,'$Q_{Tmin}$ = '+ str(Emin) +'m$^3$/s', size=15)
plt.text(0.4,-1.075,'$Q_m$ = '+ str(F) +'m$^3$/s', size=15)

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=plt.figaspect(1)*0.7)
ax = Axes3D(fig)
plt.rcParams['axes.edgecolor']='white'
plt.rcParams["figure.figsize"] = [10,8]

ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

ax.xaxis.pane.set_edgecolor('w')
ax.yaxis.pane.set_edgecolor('w')
ax.zaxis.pane.set_edgecolor('w')

sl = (FEV/2)**0.5

a = [sl, sl]
b = [sl, sl]
c = [2, 0]

d = [sl, 0]
e = [sl, sl]
f = [0, 0]

g = [sl, sl]
h = [sl, 0]
i = [0, 0]

ax.plot(a, b, c, '--', color = 'k')
ax.plot(d, e, f, '--', color = 'k')
ax.plot(g, h, i, '--', color = 'k')

x = [sl, sl, sl, 0, 0, 0, sl, sl, 0, 0, 0, 0]
y = [sl, 0, 0, 0, 0, sl, sl, 0, 0, 0, sl, sl]
z = [2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 2]

ax.plot(x, y, z, color = 'k')

ax.text(5*(sl/9), -5*(sl/9), 0, 'Side-length [m]', size=13)
ax.text(-sl/4, sl/4, 0, 'Side-length [m]', size=13)
ax.text(-0.02*sl, 1.01*sl, 0.8, 'Depth [m]',size=13)

ax.text(7*(sl/10), 5*(sl/4), 1, ''+str(int(round(sl)))+'m', size=13)
ax.text(14*(sl/10), 6*(sl/10), 1, ''+str(int(round(sl)))+'m', size=13)

ax.set_zticks([0, 2])

ax.set_xlim(sl,0)
ax.set_ylim(0,sl)
ax.set_zlim(0,10)