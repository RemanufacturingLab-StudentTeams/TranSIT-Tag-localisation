import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def polynomial(phi, *params):
    """Polynomial function for curve fitting"""
    return sum(p * phi**i for i, p in enumerate(params))

def calculate_rms(RSSI_true, RSSI_pred):
    """Calculate RMS error"""
    return np.sqrt(np.mean((RSSI_true - RSSI_pred)**2))

# Read the CSV file with semicolon separator
df = pd.read_csv('RSSI-Phi-120.csv', sep=';')

# Print column names to see what's available
print("Available columns in the CSV file:")
print(df.columns.tolist())

# Get Phi and RSSI values
phi = df['phi'].values
RSSI = df['RSSI'].values

# Create a figure for plotting
plt.figure(figsize=(12, 8))
plt.scatter(phi, RSSI, color='blue', label='Original Data')

# Dictionary to store results
results = {}

# Perform curve fitting for degrees 2 to 3
for degree in range(2, 4):
    # Initial guess for parameters (all zeros)
    p0 = np.zeros(degree + 1)
    
    # Fit the curve
    popt, _ = curve_fit(polynomial, phi, RSSI, p0=p0)
    
    # Generate points for smooth curve
    phi_smooth = np.linspace(min(phi), max(phi), 100)
    RSSI_smooth = polynomial(phi_smooth, *popt)
    
    # Calculate RMS error
    RSSI_pred = polynomial(phi, *popt)
    rms = calculate_rms(RSSI, RSSI_pred)
    
    # Store results
    results[degree] = {
        'coefficients': popt,
        'rms': rms,
        'equation': ' + '.join([f'{popt[i]:.6f}φ^{i}' for i in range(len(popt))])
    }
    
    # Plot the fitted curve
    plt.plot(phi_smooth, RSSI_smooth, label=f'{degree}th degree (RMS: {rms:.4f})')

plt.xlabel('Phi (φ)')
plt.ylabel('RSSI')
plt.title('Polynomial Curve Fitting for RSSI vs Phi')
plt.legend()
plt.grid(True)
plt.show()

# --- Second plot: Shift both fitted curve and data so fit's max is zero ---

results_fit_and_data_shifted = {}

for degree in range(2, 4):
    # Retrieve the original fit parameters
    popt = results[degree]['coefficients']
    # Generate a dense range of phi for finding the max
    phi_dense = np.linspace(min(phi), max(phi), 1000)
    RSSI_fit_dense = polynomial(phi_dense, *popt)
    max_fit = np.max(RSSI_fit_dense)
    # Shift the polynomial: subtract max_fit from the constant term
    popt_shifted = popt.copy()
    popt_shifted[0] -= max_fit
    # Shift the data by the same amount
    RSSI_shifted = RSSI - max_fit
    # Evaluate shifted fit
    RSSI_fit_shifted = polynomial(phi_dense, *popt_shifted)
    # Calculate RMS error for shifted fit (on shifted data)
    RSSI_pred_shifted = polynomial(phi, *popt_shifted)
    rms_shifted = calculate_rms(RSSI_shifted, RSSI_pred_shifted)
    # Store results
    results_fit_and_data_shifted[degree] = {
        'coefficients': popt_shifted,
        'rms': rms_shifted,
        'equation': ' + '.join([f'{popt_shifted[i]:.6f}φ^{i}' for i in range(len(popt_shifted))])
    }
    # Plot shifted fit and shifted data in a separate figure for each degree
    plt.figure(figsize=(12, 8))
    plt.plot(phi_dense, RSSI_fit_shifted, label=f'{degree}th degree shifted fit (max→0, RMS: {rms_shifted:.4f})')
    plt.scatter(phi, RSSI_shifted, color='green', label='Data shifted by fit max (max of fit→0)')
    plt.xlabel('Phi (φ)')
    plt.ylabel('Shifted RSSI (data and fit, max of fit→0)')
    plt.title(f'{degree}th Degree: Data and Polynomial Fit Shifted so Fit Max is Zero')
    plt.legend()
    plt.grid(True)
    plt.show()

# Print results for shifted fitted curves and data
print("\nResults for each polynomial degree (data and fit shifted so fit max→0):")
print("-" * 50)
for degree, result in results_fit_and_data_shifted.items():
    print(f"\n{degree}th degree polynomial (fit and data shifted):")
    print(f"Shifted Fit: RSSI = {result['equation']}")
    print(f"RMS Error: {result['rms']:.4f}")