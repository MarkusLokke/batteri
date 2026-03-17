import numpy as np

x = np.ones(90)
z = np.zeros((9,10))

for i in range(9):
    z[i] = x[i*10:(i+1)*10]

print(np.shape(z))
print(z)
