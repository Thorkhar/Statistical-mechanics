import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

class SolarCell:
    def __init__(self, T:int):
        self.T = T
        self.beta = 1/(T*8.62 * 10**(-5))
        self.E_photon = 2.701*8.62 * 10**(-5)*T

    def n_integrand(self, x):  # DoS function to integrate over
        y = (x ** 2) / (np.exp(self.beta * x) - 1)
        return y

    def N_integral(self, lower_limit, upper_limit):
        return quad(self.n_integrand, lower_limit, upper_limit)

    def calculate_efficiency(self):
        eff_results = []
        N_total = self.N_integral(0.001, np.inf)

        for i in np.arange(0.001, 5, 0.001):
            N_abs = self.N_integral(i, np.inf)
            nabs = N_abs[0] / N_total[0]
            eff = nabs * (i / self.E_photon)
            eff_results.append(eff)

        return eff_results

    def calculate_max_eff(self, values_list):  # takes regular Python list as input
        np_results_array = np.array(values_list)
        max_value_index = np.argmax(np_results_array)
        optimal_bandgap = (max_value_index + 1) * 0.001
        max_value = np_results_array[max_value_index]
        return optimal_bandgap, max_value

    def create_plot(self, y_values,):
        plt.plot(np.arange(0.001, 5, 0.001), y_values, 0.001)
        plt.xlabel('Bandgap energy (eV)')
        plt.ylabel('Efficiency')
        plt.show()


sun = SolarCell(5800)
sirius = SolarCell(9940)

efficiency_sun = sun.calculate_efficiency()
max_eff_sun, ideal_gap_sun = sun.calculate_max_eff(efficiency_sun)
print(max_eff_sun, ideal_gap_sun)
#sun.create_plot(efficiency_sun)

efficiency_sirius = sirius.calculate_efficiency()
max_eff_sirius, ideal_gap_sirius = sirius.calculate_max_eff(efficiency_sirius)
print(max_eff_sirius, ideal_gap_sirius)
sirius.create_plot(efficiency_sirius)