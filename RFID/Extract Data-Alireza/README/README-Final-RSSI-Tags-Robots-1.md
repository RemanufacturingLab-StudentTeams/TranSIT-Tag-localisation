# RFID RSSI Logger & Robot Tag Mapping Tool

This Python script interfaces with a **TSL RAIN RFID reader** to collect RSSI data from tags. It records tag readings along with spatial metadata (antenna position, tag position, rotation, etc.) and organizes the output into an Excel file grouped by tag ID.

## 🚀 Key Features

- Serial communication with TSL RFID reader via COM port
- User-defined:
  - Antenna position (`X`, `Y`, `Z`) and orientation (`Z` rotation)
  - Reader power level and port
  - Tag location (`X`, `Y`) per unique tag
- Real-time inventory using `$ba -go` command
- RSSI extraction and scaling
- Measurement log exported to an `.xlsx` file:
  - All data in one sheet
  - Per-tag sheets for individual analysis
- Graceful shutdown and save on `Ctrl+C`

## 🔧 Hardware Requirements

- TSL RAIN RFID Reader (USB/Serial)
- UHF RFID tags
- Compatible PC with Python 3.x

## 📦 Software Requirements

- Python 3.8+
- `pyserial`
- `pandas`
- `openpyxl`

Install dependencies with:

```bash
pip install pyserial pandas openpyxl
