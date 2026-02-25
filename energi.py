import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

price = pd.read_csv('energi.csv',usecols=[3], names=['price'])
pseries = price['price']
pseries2 = np.zeros(int(len(pseries)/4))
pseries3 = np.zeros(24)

for i in range(int(len(pseries2))):
    pseries2[i] = np.mean((pseries[i*4],pseries[i*4+1],pseries[i*4+2],pseries[i*4+3]))

for i in range(24):
    pseries3[i] = np.mean(pseries2[i::24])

t = np.linspace(0,23,24)

print(np.mean(pseries2[23::24]))


plt.plot(t,pseries3)
plt.show()