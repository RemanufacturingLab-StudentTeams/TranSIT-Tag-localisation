# RSSI Calibration

This module fits empirical models to characterize how RSSI varies with distance, azimuth angle (phi), and antenna orientation (alpha).

## Scripts

### Distance Calibration
- **`distance-curve-fitting.py`** - Fits a 6th-order polynomial to RSSI vs distance data
  - Input: `data/rssi-distance-lab.xlsx` or `data/rssi-distance-company.xlsx`
  - Output: Polynomial coefficients, RMS error, curve plot (`f1.pdf`)

### Azimuth Angle Calibration (Phi)
- **`phi-curve-fitting.py`** - Fits 2nd/3rd degree polynomials to RSSI vs azimuth angle
- **`phi-curve-fitting-normalized.py`** - Normalized variant where max(fit) = 0 dBm
  - Input: CSV files in `data/` (e.g., `RSSI-Phi-120.csv`)
  - Output: Polynomial coefficients, RMS error, visualization

### Antenna Orientation Calibration (Alpha)
- **`alpha-curve-fitting.py`** - Fits sinusoidal (cosine) model to RSSI vs antenna orientation
- **`alpha-curve-fitting-normalized.py`** - Normalized variant with both cosine and sine models
  - Input: `data/RSSI-alpha-0.7-y=150.csv`
  - Output: Model parameters, RMS error, visualization

## Data Files

| File | Description |
|------|-------------|
| `rssi-distance-lab.xlsx` | RSSI vs distance measurements (laboratory) |
| `rssi-distance-company.xlsx` | RSSI vs distance measurements (company site) |
| `RSSI-Phi-*.csv` | RSSI vs azimuth angle at various configurations |
| `RSSI-alpha-*.csv` | RSSI vs antenna orientation data |

## Mathematical Models

### RSSI vs Distance (F1)
```
RSSI(d) = a6*d^6 + a5*d^5 + a4*d^4 + a3*d^3 + a2*d^2 + a1*d + a0
```

### RSSI vs Azimuth Angle (F2)
```
RSSI(phi) = a*phi^2 + b*phi + c  (normalized to max = 0 dBm)
```

### RSSI vs Antenna Orientation (F3)
```
RSSI(alpha) = A * cos(omega * alpha + phase) + offset
```

## Usage

```bash
# Fit distance model
python distance-curve-fitting.py

# Fit azimuth angle model (normalized)
python phi-curve-fitting-normalized.py

# Fit orientation model (normalized)
python alpha-curve-fitting-normalized.py
```
