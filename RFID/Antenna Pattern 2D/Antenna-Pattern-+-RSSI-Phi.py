import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Function to calculate RSSI based on distance
def rssi_distance(d):
    return -30.625214*d**0 + -66.049565*d**1 + 47.932897*d**2 + 6.934334*d**3 + -23.319914*d**4 + 9.552617*d**5 + -1.222853*d**6

# Function to calculate RSSI based on angle
def rssi_angle(phi):
    return -58.322821 + 0.038186*phi - 0.003704*phi**2

# Function to solve for distance given RSSI
def solve_distance(rssi):
    def equation(d):
        return rssi_distance(d) - rssi
    return fsolve(equation, 1.0)[0]

# Generate RSSI values from -40 to -70 with 5dB steps
rssi_values = np.arange(-40, -71, -5)

# Generate angles from -60 to 60 degrees
angles = np.linspace(-60, 60, 121)
angles_rad = np.radians(angles)

# Create the plot
plt.figure(figsize=(12, 12))

# Plot for each RSSI value
for rssi_received in rssi_values:
    # Calculate r using the distance formula
    r = solve_distance(rssi_received)
    
    # Calculate RSSI_phi for each angle
    rssi_phi = np.array([rssi_angle(phi) for phi in angles])
    
    # Find maximum RSSI value
    rssi_max = np.max(rssi_phi)
    
    # Calculate signal loss
    signal_loss = rssi_max - rssi_phi
    
    # Calculate RSSI_a
    rssi_a = rssi_received + signal_loss
    
    # Calculate distances for each RSSI_a
    distances = np.array([solve_distance(rssi) for rssi in rssi_a])
    
    # Calculate x and y coordinates
    x = distances * np.sin(angles_rad)
    y = distances * np.cos(angles_rad)
    
    # Plot the line
    plt.plot(x, y, label=f'RSSI = {rssi_received} dBm')

# Plot transmitter location
plt.plot(0, 0, 'ko', label='Transmitter', markersize=10)

# Customize the plot
plt.grid(True)
plt.axis('equal')
plt.xlabel('X Distance (meters)')
plt.ylabel('Y Distance (meters)')
plt.title('Signal Path Visualization for Different RSSI Values')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Show the plot
plt.show()

# Print information for each RSSI value
print("\nCalculated distances for each RSSI value:")
for rssi_received in rssi_values:
    r = solve_distance(rssi_received)
    print(f"RSSI = {rssi_received} dBm: r = {r:.2f} meters")
