import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.patches import Polygon

# Get RSSI input from user
while True:
    try:
        rssi_received = float(input("Enter the RSSI value (dBm): "))
        if -100 <= rssi_received <= 0:  # Reasonable range for RSSI
            break
        else:
            print("Please enter an RSSI value between -100 and 0 dBm.")
    except ValueError:
        print("Please enter a valid number.")

# Calculate RMS-RSSI using the provided formula
rms_rssi = 0.0000330307 * np.exp(-0.154 * rssi_received) + 0.9145 + 1.5 + 2 + 1

# Get alpha value
while True:
    try:
        alpha = float(input("Enter the alpha value in degrees (measured from Y-axis): "))
        if 0 <= alpha <= 90:
            break
        else:
            print("Please enter an angle between 0 and 90 degrees.")
    except ValueError:
        print("Please enter a valid number.")

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
    return fsolve(equation, 0.5, maxfev=1000)[0]

# Calculate upper and lower RSSI values
upper_rssi = rssi_received + rms_rssi
lower_rssi = rssi_received - rms_rssi

# Generate angles from -alpha to alpha degrees
angles = np.linspace(-alpha, alpha, int(alpha * 2 + 1))
angles_rad = np.radians(angles)

# Create the plot
plt.figure(figsize=(12, 12))

# Function to calculate and plot a single curve
def plot_curve(rssi_val, style='-', label=None):
    # Calculate r using the distance formula
    r = solve_distance(rssi_val)
    
    # Calculate RSSI_phi for each angle
    rssi_phi = np.array([rssi_angle(phi) for phi in angles])
    
    # Find maximum RSSI value
    rssi_max = np.max(rssi_phi)
    
    # Calculate signal loss
    signal_loss = rssi_max - rssi_phi
    
    # Calculate RSSI_a
    rssi_a = rssi_val + signal_loss
    
    # Calculate distances for each RSSI_a
    distances = np.array([solve_distance(rssi) for rssi in rssi_a])
    
    # Calculate x and y coordinates
    x = distances * np.sin(angles_rad)
    y = distances * np.cos(angles_rad)
    
    # Plot the line
    plt.plot(x, y, style, label=label)
    return x, y

# Plot all three curves
x_upper, y_upper = plot_curve(upper_rssi, '-', f'Upper (RSSI + RMS)')
x_lower, y_lower = plot_curve(lower_rssi, '-', f'Lower (RSSI - RMS)')
x_nominal, y_nominal = plot_curve(rssi_received, '--', f'Nominal RSSI')

# Plot transmitter location
plt.plot(0, 0, 'ko', label='Transmitter', markersize=10)

# Plot ±alpha lines
max_dist = max(max(abs(x_upper)), max(abs(y_upper))) * 1.1
x_alpha = np.array([-max_dist, max_dist])
y_alpha = x_alpha / np.tan(np.radians(alpha))
y_minus_alpha = -x_alpha / np.tan(np.radians(alpha))

plt.plot(x_alpha, y_alpha, '--', color='gray', alpha=0.5, label=f'{alpha}° reference')
plt.plot(x_alpha, y_minus_alpha, '--', color='gray', alpha=0.5, label=f'-{alpha}° reference')

# Create polygon for the intersection area
# Find points within ±alpha range
mask = (angles >= -alpha) & (angles <= alpha)
polygon_points = np.column_stack((
    np.concatenate([x_upper[mask], x_lower[mask][::-1]]),
    np.concatenate([y_upper[mask], y_lower[mask][::-1]])
))

# Add the polygon with hatching
polygon = Polygon(polygon_points, facecolor='lightblue', edgecolor='none', 
                 hatch='//////', alpha=0.3, label='Intersection Area')
plt.gca().add_patch(polygon)

# Customize the plot
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle=':', alpha=0.3)

# Calculate the actual bounds of the curves
x_min = min(min(x_upper), min(x_lower), min(x_nominal))
x_max = max(max(x_upper), max(x_lower), max(x_nominal))
y_min = min(min(y_upper), min(y_lower), min(y_nominal))
y_max = max(max(y_upper), max(y_lower), max(y_nominal))

# Add some padding to the bounds
x_padding = (x_max - x_min) * 0.1
y_padding = (y_max - y_min) * 0.1

# Ensure the origin is included in the plot
x_min = min(x_min - x_padding, 0)
x_max = max(x_max + x_padding, 0)
y_min = min(y_min - y_padding, 0)
y_max = max(y_max + y_padding, 0)

# Set axis limits based on actual curve bounds
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)

plt.xlabel('X Distance (meters)')
plt.ylabel('Y Distance (meters)')
plt.title(f'Signal Path Visualization with RSSI = {rssi_received} dBm (±{rms_rssi} dBm RMS)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Show the plot
plt.show()

# Print information
print("\nCalculated distances:")
print(f"Nominal RSSI = {rssi_received} dBm: r = {solve_distance(rssi_received):.2f} meters")
print(f"Upper RSSI = {upper_rssi} dBm: r = {solve_distance(upper_rssi):.2f} meters")
print(f"Lower RSSI = {lower_rssi} dBm: r = {solve_distance(lower_rssi):.2f} meters")
