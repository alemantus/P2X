'''
Created on:

Author: Yi Zheng, Department of Wind and Energy Systems, DTU

'''
import math
import matplotlib.pyplot as plt
import numpy as np

# Fixed parameters
p_0 = 101325
R = 8.314
F = 96485 # Faraday constant
A = 0.25 # Cell area
T = 363.15 # Temperature, K
p = 30 * p_0 # pressure, Pa
p_H2O = 10 ** (-0.645) * p_0

E_0_T = 1.5184 - 1.5421e-3 * T + 9.523e-5 * T * math.log(T) + 9.84e-8 * T ** 2
E_rev = E_0_T + R * T / (2 * F) * math.log((p - p_H2O) ** 1.5 / (p_H2O))

def U(i):
    '''
    :param i: Current density
    :return: Cell voltage
    '''
    r1 = 8.05e-5  # ohm m2
    r2 = -2.5e-7  # ohm m2/celcius
    s = 0.19  # V
    t1 = 1.002  # A-1 m2
    t2 = 8.424  # A-1 m2 celcius
    t3 = 247.3  # A-1 m2 celcius **2

    U = E_rev + (r1 + r2 * (T - 273.15)) * i + s * math.log(
    (t1 + t2 / (T - 273.15) + t3 / (T - 273.15) ** 2) * i + 1, 10)
    return U

i_range = np.linspace(500, 5000, 20)
I_range = i_range * A

# 1. Voltage vs current
Voltage = []
for current_density in i_range:
    print(current_density)
    Voltage.append(U(i = current_density))
plt.plot(I_range, Voltage, label='Voltage')
plt.ylabel('Voltage(V)')
plt.xlabel('Current(A)')
plt.legend()
plt.show()

