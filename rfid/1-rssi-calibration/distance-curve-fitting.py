import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib
# from Polyfit.polyfit import PolynomRegressor, Constraints

import pdb

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 20}

matplotlib.rc('font', **font)

def polynomial(d, *params):
    """Polynomial function for curve fitting"""
    return sum(p * d**i for i, p in enumerate(params))
    #return params[0] * np.exp(params[1]*d) - params[2]

def calculate_rms(RSSI_true, RSSI_pred):
    """Calculate RMS error"""
    return np.sqrt(np.mean((RSSI_true - RSSI_pred)**2))

# Read the Excel file
# Replace 'your_file.xlsx' with your actual Excel file name
df = pd.read_excel('Filtred-RSSI-Data-Lab.xlsx')

# Get Distance and RSSI values
d = df['Distance'].values[::1]
RSSI = df['RSSI'].values[::1]
# d_av = []
# RSSI_av = []
# for i in range(len(d)):
#     if i==0:
#         d_sum = d[i]
#         RSSI_sum = RSSI[i]
#         num = 1
#     elif d[i] == d[i-1]:
#         d_sum += d[i]
#         RSSI_sum += RSSI[i]
#         num += 1
#     else:
#         d_av.append(d_sum/num)
#         RSSI_av.append(RSSI_sum/num)
#         d_sum = d[i]
#         RSSI_sum = RSSI[i]
#         num = 1
# d = np.array(d_av)
# RSSI = np.array(RSSI_av)


# Create a figure for plotting
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot()
plt.scatter(d, RSSI,marker='.',s=20,color='black', label='Measured data')

# Dictionary to store results
results = {}

# Perform curve fitting for degrees 2 to 6
for degree in [6]:
    # Fit polynomial using numpy
    popt = np.polyfit(d, RSSI, degree)
    # Generate points for smooth curve
    d_smooth = np.linspace(min(d), max(d), 100)
    RSSI_smooth = np.polyval(popt, d_smooth)
    # Calculate RMS error
    RSSI_pred = np.polyval(popt, d)
    rms = calculate_rms(RSSI, RSSI_pred)
    
    # Store results
    results[degree] = {
        'coefficients': popt,
        'rms': rms,
        'equation': ' + '.join([f'{p:.6f}d^{degree-i}' for i, p in enumerate(popt)])
    }
    
    # Plot the fitted curve
    plt.plot(d_smooth, RSSI_smooth, color='black', label=f'{degree}th order polynomial (RMS: {rms:.4f})')

    
plt.xlabel(r'Distance, $d$ [m]',fontsize=20)
plt.ylabel(r'RSSI factor $F_1(d)$ [dBm]',fontsize=20)
#plt.title('Polynomial Curve Fitting for RSSI vs Distance')
plt.legend(fontsize=20)
plt.grid(True)
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')
plt.tight_layout()
plt.savefig('f1.pdf')
plt.show()

# Print results
print("\nResults for each polynomial degree:")
print("-" * 50)
for degree, result in results.items():
    print(f"\n{degree}th degree polynomial:")
    print(f"RSSI = {result['equation']}")
    print(f"RMS Error: {result['rms']:.4f}")
