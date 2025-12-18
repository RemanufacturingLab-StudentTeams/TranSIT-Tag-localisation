# RFID Tag Localisation Module

This module implements UHF RFID tag localisation using the **Robust passive UHF RFID tag localisation by intersecting RSSI indexed antenna sensitivity regions** method.

## Overview

The localisation algorithm works by:
1. Characterizing the antenna's RSSI response as functions of distance, azimuth angle, and antenna orientation
2. Extracting RSSI measurements from tags using a TSL RAIN RFID reader
3. Modeling measurement uncertainty
4. Computing tag positions by intersecting antenna sensitivity regions

## Module Structure

The workflow is organized into sequential stages:

| Folder | Purpose |
|--------|---------|
| `1-rssi-calibration/` | Fit empirical RSSI models for distance (D), azimuth (Phi), and orientation (Alpha) |
| `2-data-extraction/` | Interface with TSL RFID reader to collect RSSI measurements |
| `3-antenna-pattern/` | Combine RSSI functions into 2D antenna patterns with visualization |
| `4-error-model/` | Model RSSI measurement uncertainty from empirical data |
| `5-localization/` | Main tag localisation algorithm using RSSI intersection |
| `experiment-data/` | Raw experimental datasets from various test configurations |

## Quick Start

1. **Calibrate RSSI functions** (stage 1):
   ```bash
   cd 1-rssi-calibration
   python distance-curve-fitting.py      # RSSI vs distance
   python phi-curve-fitting-normalized.py # RSSI vs azimuth angle
   python alpha-curve-fitting-normalized.py # RSSI vs antenna orientation
   ```

2. **Collect tag data** (stage 2):
   ```bash
   cd 2-data-extraction
   python rssi-tag-logger.py  # Interactive RSSI collection
   ```

3. **Visualize antenna patterns** (stage 3):
   ```bash
   cd 3-antenna-pattern
   python antenna-pattern-rssi-phi.py
   ```

4. **Run localisation** (stage 5):
   ```bash
   cd 5-localization
   python tag-localization-intersection.py
   ```

## Hardware Requirements

- TSL RAIN RFID Reader (USB/Serial)
- UHF RFID passive tags
- PC with Python 3.8+

## Reference

The algorithm is described in:
> Alireza Beheshti Shirazi, Rufus Fraanje, Jenny Coenen, *Robust passive UHF RFID tag localisation by intersecting RSSI indexed antenna sensitivity regions*, Procedia Computer Science, 7th International Conference on Industry of the Future and Smart Manufacturing, 2026.
