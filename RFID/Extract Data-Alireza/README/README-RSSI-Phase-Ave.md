# RFID Data Logger with RSSI & Phase Averaging

This Python script collects real-time RFID data from a TSL reader, logging both **RSSI** and **Phase** values. It is tailored for robotic platforms and includes 3D robot position input, distance calculation, and **per-distance averaging** of RSSI and phase for analysis.

## 🧩 Key Features

- Serial communication with **TSL RAIN RFID reader**
- Logs:
  - RSSI (scaled)
  - Phase (raw hexadecimal and decimal)
  - Robot position and orientation
- Computes **average RSSI and phase per distance**
- Automatically saves data to `.csv` on `Ctrl+C`
- Clean CSV export with sortable and readable format

## 📐 Inputs Required

1. **Antenna configuration**
   - Antenna port (1–4)
   - Reader power (0–3000)
2. **Robot metadata**
   - X, Y, Z position
   - Z-axis rotation
3. **Optional session note**

## 🧮 Output Fields

The logged data includes:

- `Tag ID`, `RSSI`, `Phase`, `Phase Decimal`
- `Antenna`
- `Robot X/Y/Z [m]`
- `Robot Rot Z [deg]`
- `Distance [m]` (from origin to robot)
- `Note` (session context)
- `Avg RSSI`, `Avg Phase Decimal` (per-distance averages)

## 📂 File Output

Upon stopping with `Ctrl+C`, the script will:
- Save data to a timestamped `.csv` file, e.g.:  
  `robot_rfid_data_250624_153322.csv`
- Print average RSSI and Phase per distance
- Sort records by distance for readability

## 📦 Requirements

- Python 3.8+
- pandas
- pyserial

Install with:

```bash
pip install pandas pyserial
