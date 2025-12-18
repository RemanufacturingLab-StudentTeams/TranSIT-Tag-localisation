# Antenna Pattern Visualization

This module combines the calibrated RSSI functions (distance, azimuth, orientation) to generate 2D antenna pattern visualizations.

## Scripts

### Combined Pattern
**`antenna-pattern-rssi-phi.py`** - Combines distance and angle RSSI models
- Generates polar contour plots of signal coverage
- Visualizes RSSI levels from -40 to -70 dBm
- Shows equivalent distance for each RSSI value

### Intersecting Pattern
**`antenna-pattern-intersecting.py`** - Variable angular range antenna pattern
- User-defined angular bounds
- Multi-level RSSI curves with directional constraints
- Useful for analyzing antenna directionality

### Single RSSI Pattern
**`antenna-pattern-unique-rssi.py`** - Focus on a single RSSI value
- Calculates equivalent distance
- Visualizes directional attenuation
- Shows signal path for specific RSSI level

### Uncertainty Visualization
**`antenna-uncertainty-alpha.py`** - Uncertainty band visualization
- Models RMS-based confidence zones
- Shaded polygon display for RSSI and angle uncertainty
- Integrates antenna orientation effects

## Underlying Models

### RSSI vs Distance
```python
def rssi_distance(d):
    # 6th-order polynomial from calibration
    return a6*d**6 + a5*d**5 + ... + a0
```

### RSSI vs Angle
```python
def rssi_angle(phi):
    # Polynomial attenuation model
    return a*phi**2 + b*phi + c
```

## Output

- Polar plots showing spatial RSSI distribution
- Figures saved to `figures/` directory

## Usage

```bash
# Generate combined antenna pattern
python antenna-pattern-rssi-phi.py

# Generate pattern with uncertainty bands
python antenna-uncertainty-alpha.py
```
