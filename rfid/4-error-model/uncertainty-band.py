import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Load the Excel file
input_file = 'rfid_data_220425_125443.xlsx'
df = pd.read_excel(input_file)

# Group by ('Antenna X [m]', 'Antenna Y [m]') and compute summary statistics for RSSI
summary = df.groupby(['Antenna X [m]', 'Antenna Y [m]'])['RSSI'].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()

# Print the summary
print(summary)

# Save the summary to a new Excel file
output_file = 'rfid_rssi_summary.xlsx'
summary.to_excel(output_file, index=False)

print(f"Summary statistics saved to {output_file}")

# --- Plot std (y) vs mean (x) ---
# Filter to only include mean > -80
filtered_summary = summary[summary['mean'] > -80]
x = filtered_summary['mean'].values
y = filtered_summary['std'].values

plt.figure(figsize=(8,6))
plt.scatter(x, y, label='Data', color='blue')
plt.xlabel('Mean RSSI')
plt.ylabel('Std of RSSI')
plt.title('Std vs Mean of RSSI at Each Antenna Location')
plt.gca().invert_xaxis()  # Reverse the x-axis
plt.legend()

plt.tight_layout()

# --- Curve fitting section ---
from scipy.optimize import curve_fit

# Define possible fitting functions

def linear(x, a, b):
    return a * x + b

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

def power_law(x, a, b):
    return a * np.power(x, b)

fit_functions = [
    ("Linear", linear),
    ("Quadratic", quadratic),
    ("Exponential", exponential),
    ("Power Law", power_law)
]

best_rms = np.inf
best_fit = None
best_params = None
best_label = None
best_func = None

for label, func in fit_functions:
    try:
        # Initial guess for parameters
        if label == "Linear":
            p0 = [1, 0]
        elif label == "Quadratic":
            p0 = [1, 1, 0]
        elif label == "Exponential":
            p0 = [1, -0.1, 1]
        elif label == "Power Law":
            p0 = [1, 1]
        else:
            p0 = None
        params, _ = curve_fit(func, x, y, p0=p0, maxfev=10000)
        y_fit = func(x, *params)
        rms = np.sqrt(np.mean((y - y_fit) ** 2))
        if rms < best_rms:
            best_rms = rms
            best_fit = y_fit
            best_params = params
            best_label = label
            best_func = func
    except Exception as e:
        continue

# Plot the best fit
if best_fit is not None:
    # Generate smooth x values for the curve
    x_smooth = np.linspace(np.min(x), np.max(x), 200)
    y_smooth = best_func(x_smooth, *best_params)
    plt.plot(x_smooth, y_smooth, color='red', label=f'Best Fit: {best_label}')
    plt.legend()
    # Print the equation and RMS in the terminal
    if best_label == "Linear":
        eqn = f"std = {best_params[0]:.3f} * RSSI + {best_params[1]:.3f}"
    elif best_label == "Quadratic":
        eqn = f"std = {best_params[0]:.3f} * RSSI² + {best_params[1]:.3f} * RSSI + {best_params[2]:.3f}"
    elif best_label == "Exponential":
        eqn = f"std = {best_params[0]:.3f} * e^({best_params[1]:.3f} * RSSI) + {best_params[2]:.3f}"
    elif best_label == "Power Law":
        eqn = f"std = {best_params[0]:.3f} * RSSI^{best_params[1]:.3f}"
    else:
        eqn = "Best fit equation"
    print(f"Best fit equation: {eqn}")
    print(f"RMS error: {best_rms:.3f}")
    print("Coefficients:")
    for i, param in enumerate(best_params):
        print(f"  param[{i}]: {param:.10f}")

    # Calculate std for RSSI values from -40 to -80 every 5 dB using the best-fit model
    print("\nEstimated std for RSSI values from -40 to -80 (every 5 dB):")
    print(f"{'RSSI':>6} {'Estimated std':>15}")
    for rssi_value in range(-40, -81, -5):
        std_value = best_func(rssi_value, *best_params)
        print(f"{rssi_value:>6} {std_value:>15.4f}")
else:
    plt.text(0.05, 0.95, "No fit succeeded", transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

plt.show()

# --- Second plot: std * 4.5 (K-score) vs mean ---
K_SCORE = 4.5

y_scaled = y * K_SCORE

plt.figure(figsize=(8,6))
plt.scatter(x, y_scaled, label='Data (std x 4.5)', color='green')
plt.xlabel('Mean RSSI')
plt.ylabel('Std of RSSI x 4.5 (K-score)')
plt.title('K-score Scaled Std vs Mean of RSSI at Each Antenna Location')
plt.gca().invert_xaxis()  # Reverse the x-axis
plt.legend()
plt.tight_layout()

# Fit the same models to the scaled data
y_best_fit = None
params_scaled = None
label_scaled = None
func_scaled = None
best_rms_scaled = np.inf

for label, func in fit_functions:
    try:
        # Initial guess for parameters
        if label == "Linear":
            p0 = [1, 0]
        elif label == "Quadratic":
            p0 = [1, 1, 0]
        elif label == "Exponential":
            p0 = [1, -0.1, 1]
        elif label == "Power Law":
            p0 = [1, 1]
        else:
            p0 = None
        params, _ = curve_fit(func, x, y_scaled, p0=p0, maxfev=10000)
        y_fit = func(x, *params)
        rms = np.sqrt(np.mean((y_scaled - y_fit) ** 2))
        if rms < best_rms_scaled:
            best_rms_scaled = rms
            y_best_fit = y_fit
            params_scaled = params
            label_scaled = label
            func_scaled = func
    except Exception as e:
        continue

# Plot the best fit for scaled data
if y_best_fit is not None:
    x_smooth = np.linspace(np.min(x), np.max(x), 200)
    y_smooth = func_scaled(x_smooth, *params_scaled)
    plt.plot(x_smooth, y_smooth, color='red', label=f'Best Fit: {label_scaled}')
    plt.legend()
    # Print the equation and RMS in the terminal
    if label_scaled == "Linear":
        eqn = f"std*4.5 = {params_scaled[0]:.3f} * RSSI + {params_scaled[1]:.3f}"
    elif label_scaled == "Quadratic":
        eqn = f"std*4.5 = {params_scaled[0]:.3f} * RSSI² + {params_scaled[1]:.3f} * RSSI + {params_scaled[2]:.3f}"
    elif label_scaled == "Exponential":
        eqn = f"std*4.5 = {params_scaled[0]:.3f} * e^({params_scaled[1]:.3f} * RSSI) + {params_scaled[2]:.3f}"
    elif label_scaled == "Power Law":
        eqn = f"std*4.5 = {params_scaled[0]:.3f} * RSSI^{params_scaled[1]:.3f}"
    else:
        eqn = "Best fit equation"
    print(f"\nBest fit equation for K-score scaled data: {eqn}")
    print(f"RMS error (scaled): {best_rms_scaled:.3f}")
    print("Coefficients (scaled):")
    for i, param in enumerate(params_scaled):
        print(f"  param[{i}]: {param:.10f}")

    # Calculate std*4.5 for RSSI values from -40 to -80 every 5 dB using the best-fit model
    print("\nEstimated std*4.5 for RSSI values from -40 to -80 (every 5 dB):")
    print(f"{'RSSI':>6} {'Estimated std*4.5':>20}")
    for rssi_value in range(-40, -81, -5):
        std_value = func_scaled(rssi_value, *params_scaled)
        print(f"{rssi_value:>6} {std_value:>20.4f}")
else:
    plt.text(0.05, 0.95, "No fit succeeded", transform=plt.gca().transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

plt.show()
