# Camera Capture Tool

Webcam image capture utility for collecting calibration and test images.

## Script

**`capture.py`** - Timed image capture with spacebar trigger

Features:
- Opens default webcam using OpenCV
- Displays live video feed
- 10-second capture window
- Press SPACE to capture immediately, or wait for timeout
- Auto-incrementing filenames (`captured_image_0.jpg`, `captured_image_1.jpg`, ...)
- Hardware transform disabled on Windows to avoid MSMF errors

## Usage

```bash
python capture.py
```

Controls:
- **SPACE** - Capture image
- **ESC** or wait 10 seconds - Exit without capture

## Output

- Captured images saved as `captured_image_N.jpg` in the current directory
- Images stored in `images/` folder for reference

## Tips

- Ensure good lighting for calibration images
- For camera calibration, capture the chessboard at various angles and distances
- Aim for 10-20 calibration images covering different orientations
