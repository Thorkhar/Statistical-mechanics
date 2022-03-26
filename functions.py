import numpy as np
import matplotlib.pyplot as plt

k = 10^(-23)
T = 5700
beta = 1/(k*T)
h_bar = 10^(-34)
x = np.linspace(0, 5, 100)
y = 2/(np.exp(beta*h_bar*x)-1)

plt.plot(x,y,'r')
plt.show()
