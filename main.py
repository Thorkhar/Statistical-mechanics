import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

class SolarCell:
    def __init__(self, T:int):
        self.T = T
        self.beta = 1/(T*8.62 * 10**(-5)) #set beta = 1/kT
        self.E_photon = 2.701*8.62 * 10**(-5)*T #set the photon energy

    def integrand(self, x):  # DoS function to integrate over
        y = (x ** 2) / (np.exp(self.beta * x) - 1) #can ignore constants as they drop out in the division anyway
        return y

    def integrate(self, lower_limit, upper_limit): #integration function
        return quad(self.integrand, lower_limit, upper_limit)

    def calculate_efficiency(self):
        eff_results = [] #create empty array for the results
        N_total = self.integrate(0.001, np.inf) #N_total integration can be kept out of the for loop to reduce computation time

        for i in np.arange(0.001, 5, 0.001):
            N_absorbed = self.integrate(i, np.inf)
            n_absorbed = N_absorbed[0] / N_total[0]
            eff = n_absorbed * (i / self.E_photon)
            eff_results.append(eff)

        return eff_results

    def calculate_max_eff(self, values_list):  # takes regular Python list as input
        np_results_array = np.array(values_list) #convert list to numpy array (argmax method works better than default python max() method
        max_value_index = np.argmax(np_results_array)
        optimal_bandgap = (max_value_index + 1) * 0.001 # multiply index by loop step size to get the bandgap energy
        max_value = np_results_array[max_value_index]
        return optimal_bandgap, max_value

def create_plot(y1, y2, color1, color2, name1, name2):
    plt.plot(np.arange(0.001, 5, 0.001), y1, label=name1, color=color1)
    plt.plot(np.arange(0.001, 5, 0.001), y2, label=name2, color=color2)
    plt.xlabel('Bandgap energy (eV)')
    plt.ylabel('Solar cell efficiency')
    plt.legend(loc="upper right")
    plt.show()

sun = SolarCell(5800)
sirius = SolarCell(9940)

efficiency_sun = sun.calculate_efficiency()
max_eff_sun, ideal_gap_sun = sun.calculate_max_eff(efficiency_sun)
print(max_eff_sun, ideal_gap_sun)

efficiency_sirius = sirius.calculate_efficiency()
max_eff_sirius, ideal_gap_sirius = sirius.calculate_max_eff(efficiency_sirius)
print(max_eff_sirius, ideal_gap_sirius)

create_plot(efficiency_sun, efficiency_sirius, 'r', 'b', 'Sun', 'Sirius A')