# RFID Data Extraction

This module interfaces with TSL RAIN RFID readers to collect RSSI and phase measurements from UHF RFID tags.

## Scripts

### Tag Logger
**`rssi-tag-logger.py`** - Main data collection tool

Features:
- Serial communication with TSL RFID reader via COM port
- User-defined antenna position (X, Y, Z) and orientation
- Configurable reader power level
- Real-time inventory using `$ba -go` command
- RSSI extraction and scaling
- Output to Excel with per-tag sheets
- Graceful shutdown with `Ctrl+C`

### Phase Averaging
**`rssi-phase-average.py`** - RSSI and phase data logger with averaging

Features:
- Robot position tracking
- Per-distance RSSI averaging
- CSV export

## Hardware Setup

1. Connect TSL RAIN RFID reader via USB
2. Note the COM port (e.g., `COM3` on Windows, `/dev/ttyUSB0` on Linux)
3. Position antenna and tags in known locations

## Usage

```bash
# Start interactive RSSI logging
python rssi-tag-logger.py
```

The script will prompt for:
- COM port
- Antenna position (X, Y, Z) and rotation
- Reader power level
- Tag positions (per unique tag ID)

## Output Format

Excel file with:
- `All_Data` sheet: Complete measurement log
- Per-tag sheets: Individual analysis data

Columns include:
- Timestamp
- Tag EPC
- RSSI (dBm)
- Antenna position
- Tag position
