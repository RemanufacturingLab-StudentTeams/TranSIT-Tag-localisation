# QR Code 3D Pose Estimation and Tracking Tool (with Excel Export)

This Python script uses a **calibrated camera** to detect QR codes in real-time, estimate their **3D position and orientation**, and visualize the coordinate axes on top of the image feed. It also records and averages pose data every 5 seconds and exports the results to an Excel file.

## 📦 Features

- Detects and decodes QR codes via OpenCV
- Uses `cv.solvePnP()` for 6DoF pose estimation
- Displays:
  - 3D axes over QR code
  - Real-time camera position (X, Y, Z) in cm
  - Rotation (roll, pitch, yaw)
  - Mean position every 5 seconds
- Saves session summary to Excel:
  - One sheet per QR code
  - One sheet with all data

## 🎯 Requirements

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy
- pandas
- xlsxwriter

Install dependencies with:

```bash
pip install opencv-python numpy pandas xlsxwriter
