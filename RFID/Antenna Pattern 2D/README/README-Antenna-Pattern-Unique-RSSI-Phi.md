# Antenna Signal Path Visualization — Single RSSI Focus

This script generates a 2D spatial visualization of the signal path for a **single user-input RSSI value**, taking into account the effects of both distance-based attenuation and antenna directionality (azimuth angle).

## 🎯 Purpose

Unlike previous scripts that simulate multiple RSSI curves, this version is ideal for analyzing how **a unique RSSI reading** translates into a specific directional coverage pattern, assuming known RSSI-to-distance and antenna-gain models.

## 📌 Features

- User inputs a specific RSSI value (e.g., -50 dBm)
- Calculates equivalent distance using an empirical 6th-order polynomial model
- Computes direction-based signal attenuation using a quadratic antenna model
- Visualizes the signal path in polar-like space (X-Y)
- Displays key metrics like:
  - Calculated distance
  - Maximum antenna gain (RSSI)
  - Signal loss range

## 🧮 Models Used

### RSSI vs Distance

```python
rssi_distance(d) = -30.625158 - 66.050159*d + 47.934702*d² + ...
