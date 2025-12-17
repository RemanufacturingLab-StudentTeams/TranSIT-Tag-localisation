# Polynomial Curve Fitting: RSSI vs Phi (Azimuth Angle)

This script performs polynomial regression to model how **RSSI varies with antenna azimuth angle (φ)**. It fits 2nd- and 3rd-degree polynomials, calculates RMS errors, and visualizes both raw and normalized fits.

## 📈 Goal

To create an empirical model \( F_2(φ) \) that captures the directional attenuation of an antenna in the azimuth plane, for use in RSSI-based localization systems.

## 🧩 Features

- Reads RSSI vs φ data from CSV
- Fits **2nd- and 3rd-degree polynomials**
- Calculates **RMS error** of each fit
- Normalizes the fit:
  - Adjusts both data and fit so **max(fit) = 0**
- Generates clean plots:
  - Original data + fits
  - Shifted (normalized) data + fits
- Prints the resulting polynomial equations

## 📂 Input Format

CSV file: `RSSI-Phi-120.csv` (semicolon-separated)

Expected columns:
- `phi`: antenna azimuth angle (degrees)
- `RSSI`: signal strength (dBm)

## 📦 Requirements

- Python 3.x
- `pandas`
- `numpy`
- `scipy`
- `matplotlib`

Install with:

```bash
pip install pandas numpy matplotlib scipy
