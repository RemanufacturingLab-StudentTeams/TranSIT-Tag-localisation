# Curve Fitting of RSSI vs Antenna Orientation (Alpha)

This script fits mathematical models (sine, cosine) to empirical RSSI data as a function of **antenna orientation angle (α)**. It performs both raw and normalized data fitting and identifies the best fit based on **RMS error**.

## 📊 Purpose

To capture and model the angular dependence of RSSI due to antenna gain pattern, using curve fitting to sinusoidal functions.

## 🧩 Key Features

- Reads RSSI vs. α data from CSV
- Fits:
  - Cosine model on original data
  - Cosine and sine models on shifted data
- Performs **grid search** over amplitude and frequency
- Uses **RMS error** to select best fit
- Automatically generates:
  - Original fit plots
  - Max-normalized fit plots
  - Equation of best fit with coefficients

## 📂 Input

CSV file: `RSSI-alpha-0.7-y=150.csv` (semicolon-separated)

Expected columns:
- `alpha` (antenna orientation in degrees)
- `RSSI` (received signal strength)

## 🧪 Fitting Models

### Cosine

\[
\text{RSSI} = A \cdot \cos(f \cdot \alpha + \phi) + C
\]

### Sine (shifted data)

\[
\text{RSSI}_{\text{shifted}} = A \cdot \sin(f \cdot \alpha + \phi) + C
\]

The fit with the **lowest RMS error** is reported.

## 📦 Requirements

- Python 3.x
- `numpy`
- `pandas`
- `matplotlib`
- `scipy`

Install with:

```bash
pip install numpy pandas matplotlib scipy
