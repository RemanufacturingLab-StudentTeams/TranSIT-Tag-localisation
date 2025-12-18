# Tag Localisation

This module implements the main RFID tag localisation algorithm using RSSI-indexed antenna sensitivity region intersection.

## Algorithm Overview

The localisation method works by:
1. Reading RSSI measurements from multiple antenna positions
2. For each measurement, determining the antenna sensitivity region (spatial area where that RSSI value could originate)
3. Finding the intersection of all sensitivity regions
4. Computing the tag position as the centroid of the intersection area
5. Applying uncertainty modeling to provide confidence bounds

## Script

**`tag-localization-intersection.py`** - Main localisation algorithm

Features:
- Automatic tag detection from RFID data
- Integration of all calibrated RSSI functions (distance, azimuth, orientation)
- Uncertainty-aware position estimation
- Multi-tag support
- Visualization of intersection regions

## Input

RFID measurement data in Excel format from `../experiment-data/`:
- Tag EPC identifiers
- RSSI values (dBm)
- Antenna positions
- Antenna orientations

## Output

- Estimated tag positions (X, Y coordinates)
- Confidence bounds based on uncertainty model
- Visualization of antenna patterns and intersection regions

## Usage

```bash
python tag-localization-intersection.py
```

The script will:
1. Load experimental data
2. Process each detected tag
3. Compute position estimates
4. Display results with visualization

## Dependencies on Other Modules

This module uses calibration data from:
- `1-rssi-calibration/` - RSSI function coefficients
- `4-error-model/` - Uncertainty parameters

## Reference

See the main RFID README for the publication reference describing this algorithm.
