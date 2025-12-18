# QR Code Tag Localisation Module

This module implements vision-based tag localisation using QR codes and camera pose estimation.

## Overview

The QR code localisation system works by:
1. Capturing images from a calibrated camera
2. Detecting QR codes in the image
3. Estimating the 6DoF pose (position and orientation) using the known QR code size
4. Transforming relative positions to global coordinates

## Module Structure

| Folder | Purpose |
|--------|---------|
| `1-camera-capture/` | Webcam image capture tool |
| `2-camera-calibration/` | Intrinsic camera parameter estimation using chessboard patterns |
| `3-qr-localization/` | Real-time QR code detection and 3D pose estimation |

## Quick Start

1. **Capture calibration images** (stage 1):
   ```bash
   cd 1-camera-capture
   python capture.py
   # Press SPACE to capture, wait 10s for timeout
   ```

2. **Calibrate camera** (stage 2):
   ```bash
   cd 2-camera-calibration
   python calibration.py
   # Outputs camera matrix and distortion coefficients
   ```

3. **Run QR localisation** (stage 3):
   ```bash
   cd 3-qr-localization
   python qr-pose-estimation.py
   # Real-time detection with pose overlay
   ```

4. **Analyze results** (stage 3):
   ```bash
   python visualization.py
   # 3D visualization and error analysis
   ```

## Hardware Requirements

- USB webcam or compatible camera
- Printed QR codes of known size
- Chessboard calibration pattern (7x6 inner corners)
- PC with Python 3.x

## Coordinate System

- Camera position is estimated relative to the QR code
- Results are exported in centimeters
- Rotation is reported as roll, pitch, yaw angles

## Output

- Real-time video feed with overlaid 3D axes
- Position and rotation displayed on screen
- Excel export with 5-second averaged measurements
- 3D visualization with error analysis
