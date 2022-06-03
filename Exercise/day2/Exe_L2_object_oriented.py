'''
Created on: 20220519

Author: Yi Zheng, Department of Wind and Energy Systems, DTU

'''
import math
import matplotlib.pyplot as plt
import numpy as np

p_0 = 101325
R = 8.314
F = 96485


class alkaline_ele():
    def __init__(self, T=363.15, p=30, A=0.37):
        '''
        Initialize an alkaline electrolyser

        :param T: Temperature (K)
        :param p: Pressure (bar)
        :param A: Cell area (m2)
        '''
        self.T = T
        self.p = p * p_0
        self.A = A

    # -----------These two functions calculate the reversible voltage. You don't have to understand them--------
    def E_rev(self, p_H2O=10 ** (-0.645) * p_0):
        '''
        Reversible potential
        '''
        E_rev = self.E_rev_0() + R * self.T / (2 * F) * math.log((self.p - p_H2O) ** 1.5 / (p_H2O))
        return E_rev

    def E_rev_0(self):
        '''
        Standard reversible potential
        Reference : Low-temperature electrolysis system modelling: A review
        '''
        E_0_T = 1.5184 - 1.5421e-3 * self.T + 9.523e-5 * self.T * math.log(self.T) + 9.84e-8 * self.T ** 2
        return E_0_T

    # -----------------------------------------------------------------------------------------------------------

    def E_cell_empirical(self,
                         r1=8.05e-5,  # ohm m2
                         r2=-2.5e-7,  # ohm m2/celcius
                         s=0.19,  # V
                         t1=1.002,  # A-1 m2
                         t2=8.424,  # A-1 m2 celcius
                         t3=247.3,  # A-1 m2 celcius **2
                         i=1000  # Current density
                         ):
        """
        An empirical model from Ulleberg

        :param r1: Electrolyte ohmic resistive parameter
        :param r2: Electrolyte ohmic resistive parameter
        :param s: over voltage parameter of electrode
        :param t1: empirical over voltage parameter of electrode
        :param t2: empirical over voltage parameter of electrode
        :param t3: empirical over voltage parameter of electrode
        :param i: current density
        :return: cell voltage
        """
        self.i = i  # This could be unnecessary
        assert (t1 + t2 / (self.T - 273.15) + t3 / (self.T - 273.15) ** 2) * self.i + 1 > 0, \
            'The term within Log function should be positive'
        U = self.E_rev() + (r1 + r2 * (self.T - 273.15)) * self.i + s * math.log(
            (t1 + t2 / (self.T - 273.15) + t3 / (self.T - 273.15) ** 2) * self.i + 1, 10)
        return U

    def Faraday_eff(self, i=1000, f1=200, f2=0.94):
        m =((1/1000)/(1/10000))**2
        eps_f = (i/self.A)**2/(f1*m+(i/self.A)**2)*f2
        return eps_f

    def hydrogen_production(self, i=1000):
        HP = (i/2*96485.3321*1.008/1000)/3600

        return HP

    def power(self, i=1000):
        power = self.E_cell_empirical(i=i)*i
        return power

    def DC_efficiency(self, i=1000):
        HP =(i/(2*F))
        DC_eff = HP*285.83*10**3/self.power(i)
        return DC_eff

    def Voltage_eff(self, i=1000):
        V_eff = self.DC_efficiency(i=i)/self.Faraday_eff(i=i)
        return V_eff

if __name__ == '__main__':
    # Add new methods in the alkaline_ele class that return different efficiencies or write your own codes.
    # Define an alkaline electrolyser
    my_ael = alkaline_ele(A = 0.25)
    i_range = np.linspace(500, 5000, 20)
    I_range = i_range * my_ael.A

    # 1. Voltage vs current
    Voltage = []
    Faraday_eff = []
    hydrogen_production_list = []
    DC_eff = []
    V_eff_list = []

    plotList = []

    for current_density in i_range:
        Voltage.append(my_ael.E_cell_empirical(i=current_density))  
        Faraday_eff.append(my_ael.Faraday_eff(i=current_density))
        hydrogen_production_list.append(my_ael.hydrogen_production(i=current_density))
        DC_eff.append(my_ael.DC_efficiency(i=current_density))
        V_eff_list.append(my_ael.Voltage_eff(i=current_density))

        



    col = 3
    rows = 2
    # Create two subplots and unpack the output array immediately
    fig = plt.figure(1,dpi=100)

    plt.subplot(rows, col, 1)
    plt.title("Original") 
    plt.plot(I_range, Voltage, label='Voltage')  
    plt.ylabel('Voltage(V)')
    plt.xlabel('Current(A)')
    plt.legend()
    plt.grid(linestyle = '-.', linewidth=0.6)


    plt.subplot(rows, col, 2)
    plt.title("Faraday efficiency vs Current") 
    plt.plot(I_range, Faraday_eff, label='Voltage')  
    plt.ylabel('Faraday efficiency')
    plt.xlabel('Current(A)')
    plt.legend()
    plt.grid(linestyle = '-.', linewidth=0.6)


    plt.subplot(rows, col, 3)
    plt.title("Hydrogen production vs Current") 
    plt.plot(I_range, hydrogen_production_list, label='Voltage')  
    plt.ylabel('Hydrogen production')
    plt.xlabel('Current(A)')
    plt.legend()
    plt.grid(linestyle = '-.', linewidth=0.6)


    plt.subplot(rows, col, 4)
    plt.title("DC efficiency vs Current") 
    plt.plot(I_range, DC_eff, label='Voltage')  
    plt.ylabel('DC efficiency')
    plt.xlabel('Current(A)')
    plt.legend()
    plt.grid(linestyle = '-.', linewidth=0.6)


    plt.subplot(rows, col, 5)
    plt.title("Voltage efficiency vs Current") 
    plt.plot(I_range, V_eff_list, label='Voltage')  
    plt.ylabel('DC efficiency')
    plt.xlabel('Current(A)')
    plt.legend()
    plt.grid(linestyle = '-.', linewidth=0.6)
    
    plt.tight_layout()

    plt.show()


    


