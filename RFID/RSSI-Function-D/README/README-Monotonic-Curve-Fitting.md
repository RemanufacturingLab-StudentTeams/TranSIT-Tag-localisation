# Monotonic Polynomial Curve Fitting: RSSI vs Distance

This script performs **6th-order polynomial regression** to model the relationship between **RSSI** and **distance**, based on experimental measurements. It’s especially useful for generating an empirical function \( F_1(d) \) in RSSI-based localization systems.

## 📈 Features

- Reads distance-RSSI pairs from an Excel sheet
- Fits a **6th-degree polynomial**
- Computes **RMS error** of the fit
- Outputs:
  - Coefficients of the polynomial
  - Fitted curve equation
  - High-quality plot (`f1.pdf`) showing measured data and fitted curve

## 📂 Input Format

Excel file: `Filtred-RSSI-Data-Lab.xlsx`

Expected columns:
- `Distance`: measured in meters
- `RSSI`: in dBm

## 📦 Requirements

- Python 3.x
- `pandas`
- `numpy`
- `matplotlib`
- `scipy`

Install dependencies with:

```bash
pip install pandas numpy matplotlib scipy
