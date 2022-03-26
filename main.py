import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

E_photon = 2
k = 8.62 * 10**(-5)
T = 5700
c =  1 #3*(10**8)
beta = 1/(k*T)
h_bar = 1 #10**(-34)

def n_integrand(x):
    #y = 2/(np.exp(beta*h_bar*x) - 1)
    y = (x**2)/(np.exp(beta*x)-1)
    return y

def N_integral(lower_limit, upper_limit):
    return quad(n_integrand, lower_limit, upper_limit)

eff_results = []
nabs_results = []
N_total = N_integral(0.001, 100000)
print(N_total[0])
print(n_integrand(0.01))
for i in np.arange(0.001,5,0.001):
    N_abs = N_integral(i, 100000)
    nabs = N_abs[0]/N_total[0]
    eff = nabs * (i/E_photon)
    eff_results.append(eff)
    nabs_results.append(nabs)

plt.plot(np.arange(0.001,5,0.001), eff_results)
plt.xlabel('Bandgap energy (eV)')
plt.ylabel('Efficiency')
plt.show()

