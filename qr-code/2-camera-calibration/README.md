# Camera Calibration

Intrinsic camera calibration using chessboard pattern detection.

## Script

**`calibration.py`** - OpenCV camera calibration

Features:
- Detects corners in chessboard pattern images (7x6 inner corners)
- Computes camera intrinsic matrix and distortion coefficients
- Applies calibration to undistort a sample image
- Saves undistorted result as `calibresult.png`

## Calibration Pattern

- Standard chessboard pattern
- **7 columns x 6 rows** of inner corners
- Print at known size for accurate results

## Input

- Chessboard images (JPG format) in `images/` folder
- Target image to undistort: `captured_image_11.jpg`

## Output

- **Console**: Camera matrix (`mtx`) and distortion coefficients (`dist`)
- **File**: `camera-matrix.txt` - Saved calibration parameters
- **Image**: `calibresult.png` - Undistorted and cropped sample

## Camera Matrix Format

The output file `camera-matrix.txt` contains:
```
Camera Matrix (mtx):
[[fx  0  cx]
 [0  fy  cy]
 [0   0   1]]

Distortion Coefficients (dist):
[k1, k2, p1, p2, k3]
```

Where:
- `fx`, `fy` - Focal lengths in pixels
- `cx`, `cy` - Principal point (image center)
- `k1-k3` - Radial distortion coefficients
- `p1-p2` - Tangential distortion coefficients

## Usage

1. Place chessboard images in `images/` folder
2. Run calibration:
   ```bash
   python calibration.py
   ```
3. Copy `camera-matrix.txt` to `3-qr-localization/` for pose estimation

## Tips

- Use 10-20 images with the chessboard at different angles
- Cover the entire field of view
- Ensure the chessboard is flat and well-lit
- Avoid motion blur
