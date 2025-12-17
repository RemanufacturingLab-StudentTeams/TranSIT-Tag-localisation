# Webcam Image Capture Tool (10s Timer with Spacebar Option)

This script captures a single webcam image using **OpenCV**. It gives the user a **10-second window** to either press the **spacebar to capture** an image or let the timer expire. The script ensures that saved image filenames don’t overwrite previous captures.

## 🧩 Features

- Opens default webcam using OpenCV
- Displays live video feed
- Waits 10 seconds for user to:
  - Press **SPACE** to capture an image
  - Or do nothing (timeout with no capture)
- Auto-increments filenames (`captured_image_0.jpg`, `captured_image_1.jpg`, ...)
- Hardware transform disabled on Windows to avoid MSMF errors

## 🖼️ Output

- A captured `.jpg` image saved to the same directory (if user presses spacebar)

## 🔧 Dependencies

- Python 3.x
- OpenCV (cv2)

Install OpenCV if needed:

```bash
pip install opencv-python
