import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

k = 8.62 * 10**(-5)  #boltzmann constant in eV/K
T = 5700 #sun temp in K
beta = 1/(k*T)
E_photon = 2.701*k*T

def n_integrand(x): #DoS function to integrate over
    y = (x**2)/(np.exp(beta*x)-1)
    return y

def N_integral(lower_limit, upper_limit):
    return quad(n_integrand, lower_limit, upper_limit)


eff_results = []
nabs_results = []
N_total = N_integral(0.001, np.inf)

for i in np.arange(0.001,5,0.001):
    N_abs = N_integral(i, np.inf)
    nabs = N_abs[0]/N_total[0]
    eff = nabs * (i/E_photon)
    eff_results.append(eff)
    nabs_results.append(nabs)

np_eff_results = np.array(eff_results)
max_eff_index = np.argmax(np_eff_results)
print((max_eff_index+1)*0.001, np_eff_results[max_eff_index])

plt.plot(np.arange(0.001,5,0.001), eff_results)
plt.xlabel('Bandgap energy (eV)')
plt.ylabel('Efficiency')
plt.show()
