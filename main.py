import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

E_photon = 2.48
k = 10^(-23)
T = 5700
beta = 1/(k*T)
h_bar = 10^(-34)

def n_integrand(x):
    y = 2 / (np.exp(beta * h_bar * x) - 1)
    return y

def N_integral(lower_limit, upper_limit):
    return quad(n_integrand, lower_limit, upper_limit)

eff_results = []
nabs_results = []
N_total = N_integral(0.001/h_bar, 10000000/h_bar)
print(N_total[0])

for i in np.arange(0.001,5,0.001):
    N_abs = N_integral(i/h_bar, 10000000/h_bar)
    work = N_abs[0] * i
    energy_available = N_total[0]*E_photon
    eff = work/energy_available
    eff_results.append(eff)

plt.plot(np.arange(0.001,5,0.001), eff_results)
plt.show()

