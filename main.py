import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

k = 8.62 * 10**(-5)  #boltzmann constant in eV/K
T = 5800 #sun temp in K
beta = 1/(k*T)
E_photon = 2.701*k*T
print(E_photon)

def n_integrand(x): #DoS function to integrate over
    y = (x**2)/(np.exp(beta*x)-1)
    return y

def N_integral(lower_limit, upper_limit):
    return quad(n_integrand, lower_limit, upper_limit)

def calculate_max_eff(values_list): #takes regular Python list as input
    np_results_array = np.array(values_list)
    max_value_index = np.argmax(np_results_array)
    optimal_bandgap = (max_value_index+1)*0.001
    max_value = np_results_array[max_value_index]
    print(optimal_bandgap, max_value)

def calculate_efficiency():
    eff_results = []
    N_total = N_integral(0.001, np.inf)

    for i in np.arange(0.001,5,0.001):
        N_abs = N_integral(i, np.inf)
        nabs = N_abs[0]/N_total[0]
        eff = nabs * (i/E_photon)
        eff_results.append(eff)

    return eff_results

def create_plot(x_values, y_values, interval):
    plt.plot(x_values, y_values, interval)
    plt.xlabel('Bandgap energy (eV)')
    plt.ylabel('Efficiency')
    plt.show()

efficiency = calculate_efficiency()

calculate_max_eff(efficiency)
create_plot(np.arange(0.001, 5, 0.001), efficiency, 0.001)


