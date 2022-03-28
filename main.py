import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Create methods for later use:
class SolarCell: #create class so no repetition is needed when treating systems with other temp
    def __init__(self, T:int):
        self.T = T
        self.beta = 1/(T*8.62 * 10**(-5)) # set beta = 1/kT
        self.E_photon = 2.7*8.62 * 10**(-5)*T # set the photon energy
        self.N_total =  2.4*((8.62 * 10**(-5) * T)**3) # calculate N_total now, instead of doing it unnecessary many times in the for loops

    def integrand(self, x):  # DoS x Bose-Einstein distribution to integrate over
        y = (x ** 2) / (np.exp(self.beta * x) - 1) # can ignore constants as they drop out in the division anyway
        return y

    def integrate(self, lower_limit, upper_limit): # integration function (quad function from scipy)
        return quad(self.integrand, lower_limit, upper_limit)

    def calculate_efficiency(self, upper_limit=np.inf, set_bandgap=0.):
        eff_results = [] # create empty list for the results

        if set_bandgap == 0: # if no bandgap is pre-set we have the single layer system
            for i in np.arange(0.001, 5, 0.001): # loop over bandgap energies between 0.001 and 5 eV in steps of 0.001
                N_absorbed = self.integrate(i, upper_limit) # calculate N for energies i to upper_limit (default infinity)
                n_absorbed = N_absorbed[0] / self.N_total
                eff = n_absorbed * (i / self.E_photon) # eff calculation according to the formula found
                eff_results.append(eff)
        else: # if a bandgap is already set we are only interested in the efficiency for that specific bandgap, no for loop needed
            N_absorbed = self.integrate(set_bandgap, upper_limit)
            eff = (N_absorbed[0] * set_bandgap)/(self.N_total * self.E_photon)
            eff_results.append(eff)
        return eff_results

    def calculate_max_eff(self, values_list):  # takes regular Python list as input, no numpy
        np_results_array = np.array(values_list) # convert list to numpy array (argmax method works better than default python max() method
        max_value_index = np.argmax(np_results_array) # find array index of the max efficiency
        optimal_bandgap = (max_value_index + 1) * 0.001 # multiply index by loop step size to get the bandgap energy
        max_value = np_results_array[max_value_index] # find max efficiency from array
        return optimal_bandgap, max_value

    def calculate_doublelayer_eff(self):
        eff_results_gap1 = []
        layer1_eff_array = self.calculate_efficiency() # regular calculation for the first layer, just as if it was a single layer system

        for i in np.arange(1.12, 5, 0.001): # loop over all 1st layer bandgaps > 1.12eV
            layer1_eff = layer1_eff_array[round((i*1000))-1] # find the corresponding 1st layer efficiency, round because Python sometimes multiplies to a float instead of integer
            layer2_eff = self.calculate_efficiency(i, 1.12)[0] # calculate the 2nd layer efficiency for the 1st layer bandgap
            total_eff = layer1_eff + layer2_eff
            eff_results_gap1.append([layer1_eff, layer2_eff, total_eff])

        return eff_results_gap1

def create_plot(n, y1, y2, name1, name2, xvalues=np.arange(0.001, 5, 0.001), y3=0, name3=''): # plot function for this specific exercise
    plt.figure(n)
    plt.plot(xvalues, y1, label=name1)
    plt.plot(xvalues, y2, label=name2)
    if y3 != 0:
        plt.plot(xvalues, y3, label=name3)
    plt.xlabel('Bandgap energy (eV)')
    plt.ylabel('Solar cell efficiency')
    if y3 != 0:
        plt.legend(loc="center right")
    else:
        plt.legend(loc="upper right")

# Calculations:
# Single layer sun-system
sun = SolarCell(5800)
efficiency_sun = sun.calculate_efficiency()
max_eff_sun, ideal_gap_sun = sun.calculate_max_eff(efficiency_sun)
print('Max efficiency of the sun system is at: ', max_eff_sun, 'eV, with an efficiency of ', ideal_gap_sun)

# Single layer sirius system
sirius = SolarCell(9940)
efficiency_sirius = sirius.calculate_efficiency()
max_eff_sirius, ideal_gap_sirius = sirius.calculate_max_eff(efficiency_sirius)
print('Max efficiency of the Sirius A system is at: ', max_eff_sirius, 'eV, with an efficiency of ', ideal_gap_sirius)

create_plot(1, efficiency_sun, efficiency_sirius, 'Sun', 'Sirius A')

# Double layer sun system
doublelayer_eff = np.array(sun.calculate_doublelayer_eff())
create_plot(2, doublelayer_eff[:,0].tolist(), doublelayer_eff[:,1].tolist(), 'Layer 1', 'Layer 2', np.arange(1.12, 5, 0.001), doublelayer_eff[:,2].tolist(), 'Combined') # Yes this could probably be neater
max_value_index = np.argmax(doublelayer_eff[:,2])
besteff = doublelayer_eff[max_value_index,2]

print('Max efficiency of the double layer system is ', besteff, ' at a 1st layer bandgap of ', max_value_index*0.001+1.13)

plt.show()