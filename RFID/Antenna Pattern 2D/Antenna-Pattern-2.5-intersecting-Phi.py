import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Get angle input from user
while True:
    try:
        angle = float(input("Enter the angle range for the curves (between 0 and 90 degrees): "))
        if 0 <= angle <= 90:
            break
        else:
            print("Please enter an angle between 0 and 90 degrees.")
    except ValueError:
        print("Please enter a valid number.")

# Function to calculate RSSI based on distance
def rssi_distance(d):
    return -30.625214*d**0 + -66.049565*d**1 + 47.932897*d**2 + 6.934334*d**3 + -23.319914*d**4 + 9.552617*d**5 + -1.222853*d**6 

# Function to calculate RSSI based on angle
def rssi_angle(phi):
    return   0.038186*phi -0.003704*phi**2

# Function to solve for distance given RSSI
def solve_distance(rssi):
    def equation(d):
        return rssi_distance(d) - rssi
    # Use a better initial guess and add maxfev parameter
    return fsolve(equation, 0.5, maxfev=1000)[0]

# Generate RSSI values from -40 to -70 with 5dB steps
rssi_values = np.arange(-40, -71, -2.5)

# Generate angles from -angle to angle degrees
angles = np.linspace(-angle, angle, int(angle * 2 + 1))
angles_rad = np.radians(angles)

# Create the plot
plt.figure(figsize=(12, 12))

# Store the maximum x and y values
max_x = 0
max_y = 0

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
    
    # Update max values
    max_x = max(max_x, max(abs(x)))
    max_y = max(max_y, max(abs(y)))
    
    # Plot the line
    plt.plot(x, y, label=f'RSSI = {rssi_received} dBm')

# Plot transmitter location
plt.plot(0, 0, 'ko', label='Transmitter', markersize=10)

# Plot ±angle lines (more subtle)
max_dist = max(max_x, max_y) * 1.1  # Add 10% margin
x_angle = np.array([-max_dist, max_dist])
y_angle = x_angle / np.tan(np.radians(angle))
y_minus_angle = -x_angle / np.tan(np.radians(angle))

# Plot the angle lines with a lighter color and dashed style
plt.plot(x_angle, y_angle, '--', color='gray', alpha=0.5, label=f'{angle}° reference')
plt.plot(x_angle, y_minus_angle, '--', color='gray', alpha=0.5, label=f'-{angle}° reference')

# Customize the plot
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle=':', alpha=0.3)

# Set axis limits
plt.xlim(-3.5, 3.5)
plt.ylim(-1, 4)

plt.xlabel('X Distance (meters)')
plt.ylabel('Y Distance (meters)')
plt.title(f'Signal Path Visualization for Different RSSI Values (±{angle}° range)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Show the plot
plt.show()

# Print information for each RSSI value
print("\nCalculated distances for each RSSI value:")
for rssi_received in rssi_values:
    r = solve_distance(rssi_received)
    print(f"RSSI = {rssi_received} dBm: r = {r:.2f} meters")
