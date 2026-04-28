import pandas as pd
import numpy as np; r = lambda s : np.round(s,0)
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
        ax.set_ylim(0,190)
        ax.set_xlim(0,23)
        ax.set_xticks(t)
        ax.grid(axis='x',color='0.9')
        fig.savefig(f'C:/Users/marku/Documents/batteri/figs/{m[i]}.png', format='png',dpi=200)
        plt.close(fig)

        fig,ax = plt.subplots()
        ax.errorbar(t, timesnitt[i], yerr=timedev[i])
        ax.set_ylabel('kWh')
        ax.set_xlabel('Time of day')
        ax.set_ylim(0,190)
        ax.set_xlim(1,23)
        ax.set_xticks(t)
        ax.grid(axis='x',color='0.9')
        fig.savefig(f'C:/Users/marku/Documents/batteri/figs/{m[i]}std.png', format='png',dpi=200)
        plt.close(fig)

primforbruk = np.array([
    37.0, 36.0, 38.0, 38.5, 38.0, 37.8,  #00,01,02,03,04,05
    37.5, 47.5, 54.5, 58.8, 58.8, 59.0,  #06,07,08,09,10,11
    58.9, 58.5, 58.5, 58.7, 56.5, 52.0,  #12,13,14,15,16,17
    49.0, 48.0, 43.5, 42.0, 42.0, 42.0]) #18,19,20,21,22,23

varmforbruk_t = np.array([
    06.0, 07.5, 09.0, 08.5, 08.5, 10.0, 
    13.5, 20.0, 18.5, 17.0, 16.0, 17.5, 
    15.5, 15.5, 15.0, 15.2, 15.0, 14.8, 
    15.3, 14.0, 09.5, 10.0, 11.5, 11.0])

varmforbruk_t /= np.sum(varmforbruk_t)

varmforbruk_u = np.array([
    29.0, 24.0, 21.0, 20.0, 22.5, 18.5, 
    27.5, 21.5, 21.0, 23.0, 21.0, 25.0, 
    25.0, 17.0, 21.5, 14.5, 09.5, 11.0, 
    08.5, 10.5, 07.5, 05.5, 04.5, 05.0, 
    06.5, 06.5, 05.0, 05.5, 05.5, 04.5, 
    04.0, 07.5, 07.0, 08.0, 04.5, 0.50, 
    06.5, 12.0, 10.0, 01.0, 05.0, 10.0, 
    08.0, 15.0, 14.5, 13.0, 17.0, 15.5, 
    18.5, 18.5, 15.5, 17.0
])

forbruk = np.zeros(365*24)

for i in range(52):
    for j in range(7):
        n = i*7*24 + j*24
        forbruk[n:n+24] = primforbruk.copy()+varmforbruk_t*varmforbruk_u[i]*24
forbruk[364*24:365*24] = forbruk[363*24:364*24]

def timediff(t):
    d = np.zeros(20)
    n = np.zeros(20)
    s = np.linspace(0,23,24)

    for i in range(20):
        t2 = t.copy()[i:]
        t2 = t2-t[i]
        d[i] = np.max(t2)
        n[i] = np.argmax(t2)

    l = np.argmax(d)
    h = n[l] + s[l]

    return l,h


def prisfunc(m=0):

    tp = timepris.copy()
    if m!=0: tp = tp[24*np.sum(dager[:m]):24*np.sum(dager[:(m+1)])]
    l = int(len(tp)/24)
    kwh = np.zeros(l)
    s=0;a=0
    f = forbruk.copy()

    for i in range(l):
        s += np.sum(np.multiply(f[i*24:(i+1)*24],tp[i*24:(i+1)*24]))
        f2 = f.copy()[i*24:(i+1)*24]
        low, high = timediff(tp[i*24:(i+1)*24])
        kwh[i] = 0.9*f2[int(high)]
        f2[int(low)] += 0.9*f2[int(high)]
        f2[int(high)] *= 0.1
        a += np.sum(np.multiply(f2,tp[i*24:(i+1)*24]))

        if i==100: print(f2[int(high)])
    
    print(np.max(kwh))

    return round(s,2),round(a,2)

prisdiff = np.zeros(13)

s,a = prisfunc()

"""for i in range(13):    
    s,a=prisfunc(m=i)
    prisdiff[i] = (1-a/s)*100
    print(m[i])
    print(r(s))
    print(r(a))
    print(r(s-a))
    print(np.round(100-100*a/s,1))
    print('--')

mnd = np.linspace(1,12,12)
fig,ax = plt.subplots()
ax.plot(mnd,prisdiff[1:])
ax.axline((6,prisdiff[0]),slope=0, linestyle='--')
ax.set_ylabel('%')
ax.set_xlabel('måned')
ax.set_xticks(mnd)
ax.set_ylim(0,6)
ax.grid(axis='x',color='0.8')
fig.savefig(f'C:/Users/marku/Documents/batteri/figs/spar.png', format='png',dpi=200)
plt.close(fig)
"""