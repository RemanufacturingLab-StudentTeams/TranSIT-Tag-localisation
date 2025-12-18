import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import filedialog
import numpy as np

# Prompt user to select the Excel file
root = tk.Tk()
root.withdraw()
excel_filename = filedialog.askopenfilename(title="Select Excel file", filetypes=[("Excel files", "*.xlsx")])
if not excel_filename:
    print("No file selected. Exiting.")
    exit(1)

# Read setup info (camera and QR code locations)
setup_info = pd.read_excel(excel_filename, sheet_name='Setup_Info')

# Extract camera and QR code coordinates
camera_row = setup_info[setup_info['Item'] == 'Camera'].iloc[0]
qr_row = setup_info[setup_info['Item'] == 'QR Code'].iloc[0]

camera_coords = [float(camera_row['X']), float(camera_row['Y']), float(camera_row['Z'])]
qr_coords = [float(qr_row['X']), float(qr_row['Y']), float(qr_row['Z'])]

# Read estimated QR code positions (relative to camera)
all_data = pd.read_excel(excel_filename, sheet_name='All_Data')

# Extract X, Y, Z positions (relative to camera)
x_rel = all_data['X_Position_cm']
y_rel = all_data['Y_Position_cm']
z_rel = all_data['Z_Position_cm']

# Convert estimated positions to global coordinates
x_est = x_rel + camera_coords[0]
y_est = y_rel + camera_coords[1]
z_est = z_rel + camera_coords[2]

# Calculate errors (Euclidean distance from each estimated point to real QR code location)
errors = np.sqrt((x_est - qr_coords[0])**2 + (y_est - qr_coords[1])**2 + (z_est - qr_coords[2])**2)
mean_error = np.mean(errors)

# Calculate per-axis errors
error_x = x_est - qr_coords[0]
error_y = y_est - qr_coords[1]
error_z = z_est - qr_coords[2]

mean_error_x = np.mean(np.abs(error_x))
mean_error_y = np.mean(np.abs(error_y))
mean_error_z = np.mean(np.abs(error_z))

# Create a single figure with three subplots for different views
fig = plt.figure(figsize=(18, 6))
views = [
    (20, 30, 'Isometric'),
    (90, -90, 'Top-down'),
    (0, 0, 'Side')
]
for i, (elev, azim, title_suffix) in enumerate(views, 1):
    ax = fig.add_subplot(1, 3, i, projection='3d')
    ax.set_xlim([-50, 150])
    ax.set_ylim([-50, 150])
    ax.set_zlim([-50, 100])
    ax.set_xticks(range(-50, 151, 10))
    ax.set_yticks(range(-50, 151, 10))
    ax.set_zticks(range(-50, 101, 10))
    ax.grid(True)
    # Draw thick black axes lines
    ax.plot([-50, 150], [0, 0], [0, 0], color='black', linewidth=2)  # X axis
    ax.plot([0, 0], [-50, 100], [0, 0], color='black', linewidth=2)  # Y axis
    ax.plot([0, 0], [0, 0], [-50, 100], color='black', linewidth=2)  # Z axis
    # Plot the origin
    ax.scatter([0], [0], [0], c='red', s=70, label='Origin (0,0,0)')
    ax.text(0, 0, 0, 'Origin', color='red')
    # Plot the camera location
    ax.scatter([camera_coords[0]], [camera_coords[1]], [camera_coords[2]], c='orange', s=100, label='Camera Location (global)')
    ax.text(camera_coords[0], camera_coords[1], camera_coords[2], 'Camera', color='orange')
    # Plot real QR code location
    ax.scatter([qr_coords[0]], [qr_coords[1]], [qr_coords[2]], c='blue', s=100, label='Real QR Code Location (global)')
    ax.text(qr_coords[0], qr_coords[1], qr_coords[2], 'QR Code (real)', color='blue')
    # Plot estimated QR code locations (global)
    ax.scatter(x_est, y_est, z_est, c='green', s=40, label='Estimated QR Code Locations (global)')
    ax.plot(x_est, y_est, z_est, c='green', alpha=0.5)
    # Draw error lines from each estimated point to the real QR code location
    for xe, ye, ze in zip(x_est, y_est, z_est):
        ax.plot([xe, qr_coords[0]], [ye, qr_coords[1]], [ze, qr_coords[2]], c='magenta', linestyle='--', alpha=0.5)
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    ax.set_title(
        f'{title_suffix} View\n'
        f'Mean Error X: {mean_error_x:.2f} cm, '
        f'Y: {mean_error_y:.2f} cm, '
        f'Z: {mean_error_z:.2f} cm'
    )
    ax.view_init(elev=elev, azim=azim)
    if i == 1:
        ax.legend()
plt.tight_layout()
plt.show() 