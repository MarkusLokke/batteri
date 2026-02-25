import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dager = [0,31,28,31,30,31,30,31,31,30,31,30,31]
m = ['00aar2025','01jan','02feb','03mar','04apr','05mai','06jun','07jul','08aug','09sep','10okt','11nov','12des']


price = pd.read_csv('energi.csv',usecols=[3], names=['price'])
timepris_temp = price['price']
timepris = np.zeros(int(len(timepris_temp)/4))
timesnitt = np.zeros((13,24))

for i in range(int(len(timepris))):
    timepris[i] = np.mean((timepris_temp[i*4],timepris_temp[i*4+1],timepris_temp[i*4+2],timepris_temp[i*4+3]))

"""for k in range(13):
    for i in range(24):
        timesnitt[k][i] = np.mean(timepris[i::24])"""

for k in range(13):
    a = int(np.sum(dager[:k])*24)
    b = int(np.sum(dager[:(k+1)])*24+1)
    if k==0:b=int(len(timepris)+1)
    for i in range(24):
        timesnitt[k][i] = np.mean(timepris[(i+a):b:24])

t = np.linspace(0,23,24)

for i in range(13):
    plt.plot(t,timesnitt[i])
    plt.title(m[i])
    plt.ylim(20,125)
    plt.savefig(f'C:/Users/marku/Documents/batteri/figs/{m[i]}.png', format='png',dpi=200)
    plt.clf()

