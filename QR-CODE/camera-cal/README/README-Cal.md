# Camera Calibration using Chessboard Images (OpenCV)

This script performs **intrinsic camera calibration** using a set of chessboard images. It computes the camera matrix and distortion coefficients, then uses them to correct lens distortion on a sample image.

## 📸 Overview

- Detects corners in chessboard pattern images (`7x6` inner corners)
- Computes:
  - **Camera matrix** (`mtx`)
  - **Distortion coefficients** (`dist`)
- Applies calibration to undistort a target image
- Saves the undistorted result as `calibresult.png`

## 🧩 Input

- Chessboard images (JPG format) in the **same folder**
- Target image to undistort: hardcoded as `captured_image_11.jpg`

## 📐 Parameters

- Pattern size: `(7, 6)` — 7 columns × 6 rows of inner corners
- Criteria for subpixel refinement: 30 iterations, ε = 0.001
- Undistortion uses `cv.getOptimalNewCameraMatrix()`

## 🛠️ Output

- Printed:
  - Camera intrinsic matrix (`mtx`)
  - Distortion coefficients (`dist`)
- Image:
  - `calibresult.png` — undistorted and cropped image

## 📦 Requirements

- Python 3.x
- OpenCV

Install with:

```bash
pip install opencv-python
