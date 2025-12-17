# Remanufacturing Lab - "TranSIT - RFID and QR-code Tag localisation"
This repository contains code to locate the position of tags. The code is being used for the development of the Tag Mapping Robot at the Smart Sustainable Manufacturing lectorate at the Hague University of Applied Sciences.
The URF RFID localisation algorithm is described in detail in: 
- Alireza Beheshti Shirazi, Rufus Fraanje, Jenny Coenen, Robust passive UHF RFID tag localisation by intersecting RSSI indexed antenna sensitivity regions, to appear in Procedia Computer Science, 7th International Conference on Industry of the Future and Smart Manufacturing, 2026.

# General Overview
This repository contains the code for UHF RFID localisation and for QR-code localisation.

# RFID Localization
1. For any RFID localization task, the antenna pattern must first be determined.
The relevant functions for the antenna pattern can be found in the RSSI-Function-D, RSSI-Function-Phi, and RSSI-Function-Alpha files.
2. To integrate these functions, refer to the Antenna Pattern 2D folder.
3. The Error-Model file provides the necessary model for handling measurement uncertainty.
4. To extract the RSSI measurements required for localization, use the Extract Data - Alireza tool.
5. With the extracted data, you can perform tag localization using the Robust RFID Tag Localization by Intersection method.
6. All data related to the experiments can be found in the Experiment Data folder.

# Attribution
- Main developmer: Alireza Beheshti
- Project manager: Rufus Fraanje

