import numpy as np
import matplotlib.pyplot as plt

k = 1.38*(10**(-23))
T = 5700
c = 3*(10**8)
beta = 1/(k*T)
h_bar = 10**(-34)
x = np.linspace(0, 5, 1000)
y = (x**2)/(np.exp(x)-1)


plt.plot(x,y,'r')
plt.show()
