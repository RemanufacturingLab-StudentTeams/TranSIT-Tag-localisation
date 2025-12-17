# Antenna Pattern & RSSI Spatial Model — Variable Angle Range

This script visualizes the spatial propagation pattern of an antenna by combining empirical models of RSSI as functions of both distance and angle. It allows users to define an angular scanning range and simulates signal coverage accordingly, providing both plots and distance calculations.

## 🧩 Key Features

- Accepts user-defined angular range (±angle degrees)
- Models RSSI with respect to:
  - **Distance (rssi_distance)** – via a sixth-order polynomial fit
  - **Angle (rssi_angle)** – via a quadratic attenuation model
- Generates signal propagation curves at multiple RSSI levels (from -40 dBm to -70 dBm, in 2.5 dB steps)
- Highlights directional bounds using ±angle reference lines
- Prints equivalent distances for each RSSI value

## 📥 Requirements

- Python 3.x
- NumPy
- Matplotlib
- SciPy

Install dependencies with:

```bash
pip install numpy matplotlib scipy
