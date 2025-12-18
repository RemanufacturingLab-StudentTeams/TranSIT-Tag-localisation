import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os

def polynomial(phi, *params):
    """Polynomial function for curve fitting"""
    return sum(p * phi**i for i, p in enumerate(params))

def calculate_rms(RSSI_true, RSSI_pred):
    """Calculate RMS error"""
    return np.sqrt(np.mean((RSSI_true - RSSI_pred)**2))

# List of CSV files to process - ADD YOUR FILE NAMES HERE
csv_files = [
    'RSSI-Phi-120.csv',  # Replace with your actual file names
    'RSSI-Phi-120-y=190.csv',
    'RSSI-Phi-170.csv',
    'RSSI-Phi-170-y=190.csv'
]

# Create empty lists to store all data
all_phi = []
all_RSSI = []
processed_files = []

# Read and combine data from specified CSV files
for file in csv_files:
    try:
        # Read each CSV file with semicolon separator
        df = pd.read_csv(file, sep=';')
        
        # Check if required columns exist
        if 'phi' not in df.columns or 'RSSI' not in df.columns:
            print(f"Warning: File {file} does not have required columns (phi, RSSI). Skipping...")
            continue
            
        # Append data from this file
        all_phi.extend(df['phi'].values)
        all_RSSI.extend(df['RSSI'].values)
        processed_files.append(file)
        print(f"Successfully read data from {file}")
        
    except Exception as e:
        print(f"Error reading {file}: {str(e)}")
        continue

if not processed_files:
    print("No files were successfully processed!")
    exit()

# Convert lists to numpy arrays
phi = np.array(all_phi)
RSSI = np.array(all_RSSI)

# Create a figure for plotting
plt.figure(figsize=(12, 8))

# Plot data points from each file with different colors
colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan']  # Add more colors if needed
markers = ['o', 's', '^', 'v', 'D', '*']  # Different markers for each file

# Create scatter plots for each file separately
for i, file in enumerate(processed_files):
    df = pd.read_csv(file, sep=';')
    color = colors[i % len(colors)]
    marker = markers[i % len(markers)]
    plt.scatter(df['phi'], df['RSSI'], 
               color=color, 
               marker=marker,
               label=f'Data from {file}', 
               alpha=0.5)

# Dictionary to store results
results = {}

# Perform curve fitting for degrees 2 to 3
for degree in range(2, 4):
    # Initial guess for parameters (all zeros)
    p0 = np.zeros(degree + 1)
    
    try:
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
        plt.plot(phi_smooth, RSSI_smooth, 
                '--', 
                linewidth=2,
                label=f'{degree}th degree fit (RMS: {rms:.4f})')
        
    except Exception as e:
        print(f"Error fitting {degree}th degree polynomial: {str(e)}")
        continue

plt.xlabel('Phi (φ)')
plt.ylabel('RSSI')
plt.title('Polynomial Curve Fitting for Combined RSSI vs Phi Data')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

# Print results
print("\nResults for each polynomial degree:")
print("-" * 50)
for degree, result in results.items():
    print(f"\n{degree}th degree polynomial:")
    print(f"RSSI = {result['equation']}")
    print(f"RMS Error: {result['rms']:.4f}")

# Print summary statistics
print("\nData Summary:")
print("-" * 50)
print(f"Total number of data points: {len(phi)}")
print(f"Files processed: {', '.join(processed_files)}")
print(f"Phi range: {min(phi):.2f} to {max(phi):.2f}")
print(f"RSSI range: {min(RSSI):.2f} to {max(RSSI):.2f}")
