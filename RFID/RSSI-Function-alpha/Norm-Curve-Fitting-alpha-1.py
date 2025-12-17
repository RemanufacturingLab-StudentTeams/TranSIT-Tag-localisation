import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Polynomial function for curve fitting
def polynomial(alpha, *params):
    return sum(p * alpha**i for i, p in enumerate(params))

def sin_func(alpha, amplitude, frequency, phase, offset):
    return amplitude * np.sin(frequency * alpha + phase) + offset

def cos_func(alpha, amplitude, frequency, phase, offset):
    return amplitude * np.cos(frequency * alpha + phase) + offset

def calculate_rms(RSSI_true, RSSI_pred):
    return np.sqrt(np.mean((RSSI_true - RSSI_pred)**2))

# Read the CSV file with semicolon separator
df = pd.read_csv('RSSI-alpha-0.7-y=150.csv', sep=';')

print("Available columns in the CSV file:")
print(df.columns.tolist())

# Get alpha and RSSI values
alpha = df['alpha'].values
RSSI = df['RSSI'].values

plt.figure(figsize=(12, 8))
plt.scatter(alpha, RSSI, color='blue', label='Original Data')

results = {}

# Fit sine and cosine functions with grid search for best frequency and amplitude
amplitude_guess = (np.max(RSSI) - np.min(RSSI)) / 2
offset_guess = np.mean(RSSI)
base_frequency = 2 * np.pi / (np.max(alpha) - np.min(alpha))

frequency_grid = np.linspace(0.1 * base_frequency, 5 * base_frequency, 20)
amplitude_grid = np.linspace(0.5 * amplitude_guess, 2 * amplitude_guess, 10)

# Only perform cosine fit grid search
best_cos_rms = np.inf
best_cos_params = None
for freq in frequency_grid:
    for amp in amplitude_grid:
        cos_p0 = [amp, freq, 0, offset_guess]
        cos_bounds = ([-np.inf, 0, -2*np.pi, -np.inf], [np.inf, 10*freq, 2*np.pi, np.inf])
        try:
            popt, _ = curve_fit(cos_func, alpha, RSSI, p0=cos_p0, bounds=cos_bounds, maxfev=10000)
            RSSI_pred = cos_func(alpha, *popt)
            rms = calculate_rms(RSSI, RSSI_pred)
            if rms < best_cos_rms:
                best_cos_rms = rms
                best_cos_params = popt
        except Exception:
            continue
if best_cos_params is not None:
    alpha_smooth = np.linspace(min(alpha), max(alpha), 100)
    RSSI_smooth = cos_func(alpha_smooth, *best_cos_params)
    equation = f'{best_cos_params[0]:.6f}*cos({best_cos_params[1]:.6f}*α + {best_cos_params[2]:.6f}) + {best_cos_params[3]:.6f}'
    results['cosine'] = {
        'label': 'Best Cosine function',
        'coefficients': best_cos_params,
        'rms': best_cos_rms,
        'equation': equation
    }
    plt.plot(alpha_smooth, RSSI_smooth, color='orange', label=f'Cosine (RMS: {best_cos_rms:.4f})')
else:
    print("Cosine fit failed for all grid values.")

plt.xlabel('Alpha (α)')
plt.ylabel('RSSI')
plt.title('Curve Fitting for RSSI vs Alpha')
plt.legend()
plt.grid(True)
plt.show()

# --- Second plot: Shift both data and cosine fit so max(cos_fit) = 0 ---
if best_cos_params is not None:
    RSSI_cos_smooth = cos_func(alpha_smooth, *best_cos_params)
    max_cos = np.max(RSSI_cos_smooth)
    # Shift both data and fit
    RSSI_shifted = RSSI - max_cos
    RSSI_cos_shifted = RSSI_cos_smooth - max_cos
    plt.figure(figsize=(12, 8))
    plt.scatter(alpha, RSSI_shifted, color='purple', label='Shifted Data (max of fit→0)')
    plt.plot(alpha_smooth, RSSI_cos_shifted, color='red', label='Cosine Fit (max→0)')
    plt.xlabel('Alpha (α)')
    plt.ylabel('Shifted RSSI (RSSI - max of fit)')
    plt.title('Data and Cosine Fit Shifted so Fit Maximum = 0')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Print shifted cosine equation
    shifted_equation = f'({best_cos_params[0]:.6f}*cos({best_cos_params[1]:.6f}*α + {best_cos_params[2]:.6f}) + {best_cos_params[3]:.6f}) - {max_cos:.6f}'
    shifted_rms = calculate_rms(RSSI_shifted, cos_func(alpha, *best_cos_params) - max_cos)
    print("\nCosine fit and data shifted so fit max=0:")
    print(f"Shifted RSSI = {shifted_equation}")
    print(f"RMS Error (shifted): {shifted_rms:.4f}")

print("\nResults for each fitted function:")
print("-" * 50)
for key, result in results.items():
    print(f"\n{result['label']}:")
    print(f"RSSI = {result['equation']}")
    print(f"RMS Error: {result['rms']:.4f}")

# --- Second plot: Normalized/shifted data ---
RSSI_shifted = RSSI - np.max(RSSI)

plt.figure(figsize=(12, 8))
plt.scatter(alpha, RSSI_shifted, color='purple', label='Shifted Data (max→0)')

results_shifted = {}

# Sine fit grid search for shifted data
best_sin_rms = np.inf
best_sin_params = None
for freq in frequency_grid:
    for amp in amplitude_grid:
        sin_p0 = [amp, freq, 0, np.mean(RSSI_shifted)]
        sin_bounds = ([-np.inf, 0, -2*np.pi, -np.inf], [np.inf, 10*freq, 2*np.pi, np.inf])
        try:
            popt, _ = curve_fit(sin_func, alpha, RSSI_shifted, p0=sin_p0, bounds=sin_bounds, maxfev=10000)
            RSSI_pred = sin_func(alpha, *popt)
            rms = calculate_rms(RSSI_shifted, RSSI_pred)
            if rms < best_sin_rms:
                best_sin_rms = rms
                best_sin_params = popt
        except Exception:
            continue
if best_sin_params is not None:
    alpha_smooth = np.linspace(min(alpha), max(alpha), 100)
    RSSI_smooth = sin_func(alpha_smooth, *best_sin_params)
    equation = f'{best_sin_params[0]:.6f}*sin({best_sin_params[1]:.6f}*α + {best_sin_params[2]:.6f}) + {best_sin_params[3]:.6f}'
    results_shifted['sine'] = {
        'label': 'Best Sine function (shifted)',
        'coefficients': best_sin_params,
        'rms': best_sin_rms,
        'equation': equation
    }
    plt.plot(alpha_smooth, RSSI_smooth, label=f'Sine (RMS: {best_sin_rms:.4f})')
else:
    print("Sine fit failed for all grid values (shifted data).")

# Cosine fit grid search for shifted data
best_cos_rms = np.inf
best_cos_params = None
for freq in frequency_grid:
    for amp in amplitude_grid:
        cos_p0 = [amp, freq, 0, np.mean(RSSI_shifted)]
        cos_bounds = ([-np.inf, 0, -2*np.pi, -np.inf], [np.inf, 10*freq, 2*np.pi, np.inf])
        try:
            popt, _ = curve_fit(cos_func, alpha, RSSI_shifted, p0=cos_p0, bounds=cos_bounds, maxfev=10000)
            RSSI_pred = cos_func(alpha, *popt)
            rms = calculate_rms(RSSI_shifted, RSSI_pred)
            if rms < best_cos_rms:
                best_cos_rms = rms
                best_cos_params = popt
        except Exception:
            continue
if best_cos_params is not None:
    alpha_smooth = np.linspace(min(alpha), max(alpha), 100)
    RSSI_smooth = cos_func(alpha_smooth, *best_cos_params)
    equation = f'{best_cos_params[0]:.6f}*cos({best_cos_params[1]:.6f}*α + {best_cos_params[2]:.6f}) + {best_cos_params[3]:.6f}'
    results_shifted['cosine'] = {
        'label': 'Best Cosine function (shifted)',
        'coefficients': best_cos_params,
        'rms': best_cos_rms,
        'equation': equation
    }
    plt.plot(alpha_smooth, RSSI_smooth, label=f'Cosine (RMS: {best_cos_rms:.4f})')
else:
    print("Cosine fit failed for all grid values (shifted data).")

plt.xlabel('Alpha (α)')
plt.ylabel('Shifted RSSI (RSSI - max)')
plt.title('Curve Fitting for Shifted RSSI vs Alpha')
plt.legend()
plt.grid(True)
plt.show()

# Print results for shifted data
print("\nResults for each fitted function (shifted data):")
print("-" * 50)
for key, result in results_shifted.items():
    print(f"\n{result['label']}:")
    print(f"Shifted RSSI = {result['equation']}")
    print(f"RMS Error: {result['rms']:.4f}")
