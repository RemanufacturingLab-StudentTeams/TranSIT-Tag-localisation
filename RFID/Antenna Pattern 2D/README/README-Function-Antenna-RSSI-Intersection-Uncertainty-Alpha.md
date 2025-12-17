# Antenna Signal Uncertainty Visualization — RSSI & Angle Model

This Python script visualizes the signal path and associated uncertainty region based on a given RSSI value and antenna directionality. It calculates a confidence zone using an empirically modeled RMS error and plots a directional "uncertainty band" bounded by angle (alpha) and RSSI variation.

## 🎯 Objective

The script aims to show the **spatial region** where an RFID tag or transmitter might lie, given:
- A received RSSI value
- Antenna directionality pattern
- Uncertainty from RSSI variability (modeled as RMS)

## 🔍 Key Features

- User inputs:
  - RSSI value (e.g., `-52`)
  - Antenna sector angle `alpha` (e.g., `30°`)
- Models distance uncertainty using an RMS-based exponential formula
- Computes and plots:
  - **Upper bound**: `RSSI + RMS`
  - **Lower bound**: `RSSI - RMS`
  - **Nominal signal path**
- Shaded polygon shows **confidence region**
- Angular limits ±alpha shown as dashed lines

## 📐 Model Functions

### RSSI vs Distance (6th-order polynomial)

```python
rssi_distance(d) = -30.625158 - 66.050159*d + 47.934702*d² + ...
