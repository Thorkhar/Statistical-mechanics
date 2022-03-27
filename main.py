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

    def calculate_efficiency(self, upper_limit=np.inf):
        eff_results = [] #create empty array for the results
        N_total = self.integrate(0.001, upper_limit) #N_total integration can be kept out of the for loop to reduce computation time

        for i in np.arange(0.001, 5, 0.001):
            N_absorbed = self.integrate(i, upper_limit)
            n_absorbed = N_absorbed[0] / N_total[0]
            eff = n_absorbed * (i / self.E_photon)
            eff_results.append(eff)

        return eff_results

    def calculate_max_eff(self, values_list):  #takes regular Python list as input, no numpy
        np_results_array = np.array(values_list) #convert list to numpy array (argmax method works better than default python max() method
        max_value_index = np.argmax(np_results_array)
        optimal_bandgap = (max_value_index + 1) * 0.001 # multiply index by loop step size to get the bandgap energy
        max_value = np_results_array[max_value_index]
        return optimal_bandgap, max_value

    def calculate_doublelayer_eff(self):
        eff_results_gap1 = []
        layer1_eff_array = self.calculate_efficiency()
        for i in np.arange(1.13, 5, 0.01): #double loop to calculate the max efficiency for different 1st layer bandgaps, calculating below 1.12eV is useless as the 2nd layer wont absorb anything there
            layer1_eff = layer1_eff_array[round((i*1000))-1]
            layer2_eff = self.calculate_efficiency(i)[1120-1] #All photons above Egap1 have been absorbed, so now the integrate from 0 to Egap 1
            total_eff = layer1_eff + layer2_eff
            eff_results_gap1.append([layer1_eff, layer2_eff, total_eff])

        return eff_results_gap1

def create_plot(n,y1, y2, color1, color2, name1, name2, xvalues=np.arange(0.001, 5, 0.001), y3=0, color3='y', name3=''):
    plt.figure(n)
    plt.plot(xvalues, y1, label=name1, color=color1)
    plt.plot(xvalues, y2, label=name2, color=color2)
    if y3 != 0:
        plt.plot(xvalues, y3, label=name3, color=color3)
    plt.xlabel('Bandgap energy (eV)')
    plt.ylabel('Solar cell efficiency')
    if y3 != 0:
        plt.legend(loc="center right")
    else:
        plt.legend(loc="upper right")

#Single layer sun-system
sun = SolarCell(5800)
efficiency_sun = sun.calculate_efficiency()
max_eff_sun, ideal_gap_sun = sun.calculate_max_eff(efficiency_sun)
print('Max efficiency of the sun system is at: ', max_eff_sun, 'eV, with an efficiency of ', ideal_gap_sun)

#Single layer sirius system
sirius = SolarCell(9940)
efficiency_sirius = sirius.calculate_efficiency()
max_eff_sirius, ideal_gap_sirius = sirius.calculate_max_eff(efficiency_sirius)
print('Max efficiency of the Sirius A system is at: ', max_eff_sirius, 'eV, with an efficiency of ', ideal_gap_sirius)

create_plot(1, efficiency_sun, efficiency_sirius, 'r', 'b', 'Sun', 'Sirius A')

#Double layer sun system
doublelayer_eff = np.array(sun.calculate_doublelayer_eff())
create_plot(2, doublelayer_eff[:,0].tolist(), doublelayer_eff[:,1].tolist(), 'r', 'g', 'Layer 1', 'Layer 2', np.arange(1.13, 5, 0.01), doublelayer_eff[:,2].tolist(), 'y', 'Combined')
max_value_index = np.argmax(doublelayer_eff[:,2])
besteff = doublelayer_eff[max_value_index,2]

print('Max efficiency of the double layer system is ', besteff, ' at a 1st layer bandgap of ', max_value_index*0.01+1.13)

plt.show()