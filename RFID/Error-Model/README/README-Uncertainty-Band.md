# RSSI Uncertainty Modeling from Empirical Data

This script performs statistical analysis of RSSI measurements collected from an RFID system to model the **uncertainty (standard deviation)** of RSSI as a function of its mean value. It fits several candidate models to the data and visualizes both raw and scaled uncertainty bands.

## 📊 Functionality Overview

- Loads RSSI data from an Excel file
- Computes summary statistics (mean, std, min, max, count) grouped by antenna location
- Fits multiple models (linear, quadratic, exponential, power law) to the relationship between **RSSI mean** and **RSSI std**
- Selects and reports the **best-fitting model** based on RMS error
- Visualizes:
  - Std vs Mean RSSI
  - Scaled uncertainty (`std * 4.5`, representing a K-score)
- Prints analytical fit equations and model coefficients

## 📂 Input

- `rfid_data_220425_125443.xlsx` — Excel file containing columns:
  - `Antenna X [m]`, `Antenna Y [m]`
  - `RSSI`

## 📤 Output

- `rfid_rssi_summary.xlsx` — Excel file containing:
  - Antenna position
  - Mean, Std, Min, Max, Count of RSSI

## 📈 Fitting Models

The script evaluates multiple curve types:

1. **Linear:**  
   \[
   \text{std} = a \cdot \text{RSSI} + b
   \]
2. **Quadratic:**  
   \[
   \text{std} = a \cdot \text{RSSI}^2 + b \cdot \text{RSSI} + c
   \]
3. **Exponential:**  
   \[
   \text{std} = a \cdot e^{b \cdot \text{RSSI}} + c
   \]
4. **Power Law:**  
   \[
   \text{std} = a \cdot \text{RSSI}^b
   \]

Each is fitted to:
- Raw standard deviation
- Scaled standard deviation (`std × 4.5`)

The best fit is selected based on minimum RMS error.

## 📦 Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- scipy
- openpyxl (for reading `.xlsx` files)

Install with:

```bash
pip install pandas numpy matplotlib scipy openpyxl
