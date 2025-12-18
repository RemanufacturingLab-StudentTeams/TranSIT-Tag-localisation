import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Function to calculate RSSI based on distance
def rssi_distance(d):
    return -30.625158 - 66.050159*d + 47.934702*d**2 + 6.931994*d**3 - 23.318448*d**4 + 9.552179*d**5 - 1.222803*d**6

# Function to calculate RSSI based on angle
def rssi_angle(phi):
    return -58.322821 + 0.038186*phi - 0.003704*phi**2

# Function to solve for distance given RSSI
def solve_distance(rssi):
    def equation(d):
        return rssi_distance(d) - rssi
    return fsolve(equation, 1.0)[0]

# Get RSSI_received from user
rssi_received = float(input("Enter the value of RSSI_received: "))

# Calculate r using the distance formula
r = solve_distance(rssi_received)

# Generate angles from -60 to 60 degrees
angles = np.linspace(-60, 60, 121)

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

# Convert angles to radians for trigonometric calculations
angles_rad = np.radians(angles)

# Calculate x and y coordinates
x = distances * np.sin(angles_rad)
y = distances * np.cos(angles_rad)

# Create the plot
plt.figure(figsize=(10, 10))
plt.plot(x, y, 'b-', label='Signal Path')
plt.plot(0, 0, 'ro', label='Transmitter')
plt.grid(True)
plt.axis('equal')
plt.xlabel('X Distance (meters)')
plt.ylabel('Y Distance (meters)')
plt.title('Signal Path Visualization')
plt.legend()
plt.show()

# Print some key information
print(f"\nCalculated distance r: {r:.2f} meters")
print(f"Maximum RSSI value: {rssi_max:.2f} dBm")
print(f"Signal loss range: {np.min(signal_loss):.2f} to {np.max(signal_loss):.2f} dBm")
