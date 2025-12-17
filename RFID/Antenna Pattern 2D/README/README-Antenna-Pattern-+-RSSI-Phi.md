# Antenna Pattern & RSSI Polar Visualization

This Python script visualizes how received signal strength (RSSI) varies spatially with respect to both distance and antenna orientation. It combines empirical polynomial models for RSSI as a function of distance and angle to generate polar contour plots of signal reachability.

## 📌 Features 

- Models RSSI based on **distance** and **azimuth angle** (`phi`)
- Simulates signal loss and signal coverage in 2D space
- Uses a polynomial-based empirical model for distance and angular attenuation
- Plots signal paths for various RSSI values (-40 dBm to -70 dBm)
- Calculates the equivalent distance for a given RSSI level
- Marks transmitter location at origin (0, 0)

## 🧮 Underlying Models

### RSSI vs Distance

The `rssi_distance(d)` function estimates the RSSI received from a distance `d` using a sixth-order polynomial.

### RSSI vs Angle

The `rssi_angle(phi)` function models directional attenuation of the antenna based on angle (in degrees), also using a polynomial.

## 📊 Visualization

The script plots the calculated 2D coverage for multiple RSSI levels. Each curve represents the spatial extent (X, Y) where a particular RSSI value is observed, taking into account antenna gain and angular signal loss.

## 📦 Requirements

- Python 3.7+
- NumPy
- Pandas
- Matplotlib
- SciPy

You can install the required packages using pip:

```
pip install numpy pandas matplotlib scipy
```