# TranSIT - RFID and QR Code Tag Localisation

This repository contains Python code for tag localisation using two complementary technologies:
- **UHF RFID** - Passive tag localisation using RSSI-indexed antenna sensitivity region intersection
- **QR Code** - Vision-based localisation using camera pose estimation

Developed by the Remanufacturing Lab at the Hague University of Applied Sciences (THUAS) for the Tag Mapping Robot project.

## Repository Structure

```
TranSIT-Tag-localisation/
├── rfid/                    # UHF RFID localisation module
│   ├── 1-rssi-calibration/  # RSSI function fitting (distance, angle, orientation)
│   ├── 2-data-extraction/   # TSL RFID reader interface
│   ├── 3-antenna-pattern/   # 2D antenna pattern visualization
│   ├── 4-error-model/       # RSSI uncertainty modeling
│   ├── 5-localization/      # Tag position estimation algorithm
│   └── experiment-data/     # Raw experimental datasets
├── qr-code/                 # QR code localisation module
│   ├── 1-camera-capture/    # Webcam image capture
│   ├── 2-camera-calibration/# Intrinsic camera parameter estimation
│   └── 3-qr-localization/   # 6DoF pose estimation and visualization
├── docs/                    # Project documentation
│   └── policy.md            # Git contribution policy
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd TranSIT-Tag-localisation

# Install dependencies
pip install -r requirements.txt
```

### RFID Localisation

See [`rfid/README.md`](rfid/README.md) for detailed instructions.

```bash
cd rfid/5-localization
python tag-localization-intersection.py
```

### QR Code Localisation

See [`qr-code/README.md`](qr-code/README.md) for detailed instructions.

```bash
cd qr-code/3-qr-localization
python qr-pose-estimation.py
```

## Hardware Requirements

### RFID Module
- TSL RAIN RFID Reader (USB/Serial)
- UHF RFID passive tags

### QR Code Module
- USB webcam or compatible camera
- Printed QR codes of known size
- Chessboard calibration pattern

## Dependencies

- Python 3.8+
- NumPy, SciPy, pandas, matplotlib
- OpenCV (for QR code module)
- pyserial (for RFID data extraction)

See `requirements.txt` for complete list.

## Publication

The RFID localisation algorithm is described in:

> Alireza Beheshti Shirazi, Rufus Fraanje, Jenny Coenen, *Robust passive UHF RFID tag localisation by intersecting RSSI indexed antenna sensitivity regions*, Procedia Computer Science, 7th International Conference on Industry of the Future and Smart Manufacturing, 2026.

## Contributing

See [`docs/policy.md`](docs/policy.md) for Git contribution guidelines, branch naming conventions, and code review requirements.

## Attribution

| Role | Name |
|------|------|
| Main Developer | Alireza Beheshti |
| Project Manager | Rufus Fraanje |

## License

This project is developed by the Smart Sustainable Manufacturing lectorate at the Hague University of Applied Sciences.
