import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dager = [0,31,28,31,30,31,30,31,31,30,31,30,31]
m = ['00aar2025','01jan','02feb','03mar','04apr','05mai',
     '06jun','07jul','08aug','09sep','10okt','11nov','12des']


price = pd.read_csv('energi.csv',usecols=[3], names=['price'])
timepris_temp = price['price']
timepris = np.zeros(int(len(timepris_temp)/4))
timesnitt = np.zeros((13,24))
timedev = np.zeros((13,24))

for i in range(int(len(timepris))):
    timepris[i] = np.mean((timepris_temp[i*4],timepris_temp[i*4+1],timepris_temp[i*4+2],timepris_temp[i*4+3]))

timepris = timepris.astype(np.float64)


for k in range(13):
    a = int(np.sum(dager[:k])*24)
    b = int(np.sum(dager[:(k+1)])*24+1)
    if k==0:b=int(len(timepris)+1)
    for i in range(24):
        timesnitt[k][i] = np.mean(timepris[(i+a):b:24])
        timedev[k][i] = np.std(timepris[(i+a):b:24])
    

t = np.linspace(0,23,24)

def prisplot():
    for i in range(13):
        fig,ax = plt.subplots()
        ax.plot(t,timesnitt[i])
        ax.set_ylabel('kWh')
        ax.set_xlabel('Time of day')
        ax.set_ylim(5,190)
        ax.set_xlim(0,23)
        ax.set_xticks(t)
        ax.grid(axis='x',color='0.9')
        fig.savefig(f'C:/Users/marku/Documents/batteri/figs/{m[i]}.png', format='png',dpi=200)
        plt.close(fig)

        fig,ax = plt.subplots()
        ax.errorbar(t, timesnitt[i], yerr=timedev[i])
        ax.set_ylabel('kWh')
        ax.set_xlabel('Time of day')
        ax.set_ylim(5,190)
        ax.set_xlim(1,23)
        ax.set_xticks(t)
        ax.grid(axis='x',color='0.9')
        fig.savefig(f'C:/Users/marku/Documents/batteri/figs/{m[i]}std.png', format='png',dpi=200)
        plt.close(fig)

#prisplot()

forbruk = np.array([
    37.0, 36.0, 38.0, 38.5, 38.0, 37.8,  #00,01,02,03,04,05
    37.5, 47.5, 54.5, 58.8, 58.8, 59.0,  #06,07,08,09,10,11
    58.9, 58.5, 58.5, 58.7, 56.5, 52.0,  #12,13,14,15,16,17
    49.0, 48.0, 43.5, 42.0, 42.0, 42.0]) #18,19,20,21,22,23

def prisfunc2(m=0):
    tp = timepris.copy()
    if m!=0: tp = tp[24*np.sum(dager[:m]):24*np.sum(dager[:(m+1)])]
    l = int(len(tp)/24)
    s=0;a=0
    f = forbruk.copy()
    for i in range(l):
        s += np.sum(np.multiply(f,tp[i*24:(i+1)*24]))
        f2 = f.copy()
        if np.argmin(tp[i*24:(i*24+12)]) < np.argmax(tp[i*24:(i+1)*24]):
            low = np.argmin(tp[i*24:(i+1)*24])
            high = np.argmax(tp[i*24:(i+1)*24])
            f2[int(low)] += 0.9*f2[int(high)]
            f2[int(high)] *= 0.1
        a += np.sum(np.multiply(f2,tp[i*24:(i+1)*24]))
    return round(s,2),round(a,2)

prisdiff = np.zeros(13)

for i in range(13):    
    s,a=prisfunc2(m=i)
    prisdiff[i] = (1-a/s)*100
    print(f'{(s-a):.0f}')

mnd = np.linspace(1,12,12)
plt.plot(mnd,prisdiff[1:])
plt.axline((6,prisdiff[0]),slope=0, linestyle='--') 
plt.ylim(0,6)
plt.show()

