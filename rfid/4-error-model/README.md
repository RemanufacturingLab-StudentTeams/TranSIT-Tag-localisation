# RSSI Error Model

This module models the measurement uncertainty of RSSI values to support robust localisation with confidence bounds.

## Script

**`uncertainty-band.py`** - Statistical analysis of RSSI uncertainty

Features:
- Loads RSSI data from experimental measurements
- Computes summary statistics (mean, std, min, max, count) grouped by antenna location
- Fits multiple candidate models to the relationship between RSSI mean and standard deviation
- Selects best-fitting model based on RMS error
- Visualizes uncertainty bands (raw and scaled)

## Fitting Models

The script evaluates four curve types:

| Model | Equation |
|-------|----------|
| Linear | `std = a * RSSI + b` |
| Quadratic | `std = a * RSSI^2 + b * RSSI + c` |
| Exponential | `std = a * exp(b * RSSI) + c` |
| Power Law | `std = a * RSSI^b` |

Each model is fitted to:
- Raw standard deviation
- Scaled standard deviation (`std * 4.5` for K-score coverage)

## Input

- `data/rfid-uncertainty-data.xlsx` - Excel file with columns:
  - `Antenna X [m]`, `Antenna Y [m]`
  - `RSSI`

## Output

- `rfid_rssi_summary.xlsx` - Summary statistics per antenna position
- Console output: Best-fit model equations and coefficients
- Visualization: Uncertainty band plots

## Usage

```bash
python uncertainty-band.py
```

## Application

The uncertainty model is used in the localisation algorithm to:
- Define confidence regions around RSSI measurements
- Weight contributions from different antenna positions
- Improve robustness against measurement noise
