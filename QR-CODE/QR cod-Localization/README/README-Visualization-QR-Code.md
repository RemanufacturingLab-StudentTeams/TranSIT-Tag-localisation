# QR Code 3D Localization Visualization & Error Analysis

This script visualizes the spatial relationship between the **camera**, the **real QR code position**, and a series of **estimated positions** from tracking data. It also calculates **per-axis errors** and plots them from three angles for analysis.

## 📦 Features

- Interactive file selection (Excel)
- Reads:
  - **Camera and QR code positions** from `Setup_Info` sheet
  - **Estimated QR positions** from `All_Data` sheet
- Converts relative positions to **global coordinates**
- Computes:
  - Euclidean error per frame
  - Mean absolute error per axis (X, Y, Z)
- 3D Visualization:
  - Isometric view
  - Top-down view
  - Side view
- Draws:
  - Origin, camera, real QR, estimated path
  - Magenta error lines per point

## 📂 Input Format

**Excel file with at least two sheets:**

### Sheet: `Setup_Info`
| Item     | X     | Y     | Z     |
|----------|-------|-------|-------|
| Camera   | 12.5  | 35.2  | 0     |
| QR Code  | 57.8  | 62.0  | 0     |

### Sheet: `All_Data`
| X_Position_cm | Y_Position_cm | Z_Position_cm |
|---------------|---------------|---------------|
| ...           | ...           | ...           |

## 📊 Output

- A 3-panel matplotlib window:
  - **Isometric View** (20°, 30°)
  - **Top-down View** (90°, -90°)
  - **Side View** (0°, 0°)
- Labeled camera, QR code, origin
- Green estimated points + error lines to real QR location
- Titles show **mean absolute error per axis**

## 🧠 Use Cases

- Evaluate the accuracy of a QR-based localization system
- Visual debugging of coordinate transformation logic
- Demonstrate tracking error trends over time
- Compare camera models or configurations

## 🧮 Dependencies

- Python 3.x
- pandas
- matplotlib
- numpy
- tkinter (standard library)

Install requirements with:

```bash
pip install pandas matplotlib numpy
