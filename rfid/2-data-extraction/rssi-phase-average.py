import serial
import serial.tools.list_ports
import signal
import sys
import time
import pandas as pd
from datetime import datetime
from math import sqrt

# Serial port configuration for an RFID reader
tsl_name = 'TSL RAIN RFID MODULE'
tsl_baudrate = 921600
tsl_bytesize = 8
tsl_parity = 'N'
tsl_stopbits = 1
tsl_timeout = 2

def find_port(portname):
    """Scan for a COM port that includes the given port name and return its device name."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if portname in str(port.description):
            print("Port found: " + port.device)
            return port.device
    raise Exception("Port not found. Check the connection.")

def calculate_checksum(command):
    """Calculate Fletcher-16 checksum for a command."""
    c0, c1 = 0, 0
    for char in command:
        c0 = (c0 + char) % 255
        c1 = (c1 + c0) % 255
    checksum = (c1 << 8) | c0
    return checksum.to_bytes(2, byteorder='big')

def send_command(command):
    """Send a command with an appended checksum to the RFID device and read the response."""
    command_with_checksum = command + calculate_checksum(command)
    ser.write(command_with_checksum + b'\x0A')  # End command with line feed
    response = ser.read(3000)  # Read the response (up to 3000 bytes)
    return response.decode('utf-8')

def init(antenna_number, power):
    """
    Set the antenna number on the RFID reader.

    Args:
    antenna_number (int): The antenna number to set.
    power (int): The power level to set.

    Raises:
    Exception: If setting the antenna fails.
    """
    inventory_command = f'$ir -bnx0 -sex0 -tax0 -slx0 -dtx1 -anx{antenna_number} -dbx{hex(power)[2:]} -trxFFFF'
    print(inventory_command)
    lines = send_command(inventory_command.encode()).split('\n')
    time.sleep(1)  # Delay for command processing
    for line in lines:
        if line.startswith('EC:'):
            error_code = line.split(': ', 1)[1]
            if error_code != '0':
                raise Exception(f"Antenna setting to {antenna_number} failed. EC: {error_code}")
            else:
                print(f"Antenna set to {antenna_number}")

def extract_tag_details(lines):
    """Extract and return tag details and parameters from response lines."""
    tags = []
    current_antenna = 'Unknown'
    bank_number = 'Unknown'
    rf_mode = 'Unknown'
    power = 'Unknown'
    for line in lines:
        if line.startswith('BH:'):
            bh_details = line.split(': ', 1)[1].split(',')
            bank_header = {part.split('=')[0].strip(): part.split('=')[1].strip() for part in bh_details}
            current_antenna = bank_header.get('A', 'Unknown')
            bank_number = bank_header.get('B', 'Unknown')
            rf_mode = bank_header.get('R', 'Unknown')
            power = bank_header.get('P', 'Unknown')
        elif line.startswith('TR:'):
            tag_details = line.split(' | ')
            tag_info = {detail.split(': ', 1)[0].strip(): detail.split(': ', 1)[1].strip() for detail in tag_details if ': ' in detail}
            tags.append({
                'Tag ID': tag_info.get('EP', 'Unknown'),
                'RSSI': tag_info.get('RI', 'Unknown'),
                'Phase': tag_info.get('PH', 'Unknown'),
                'Antenna': current_antenna
            })
        elif line.startswith('EC:'):
            error_code = line.split(': ', 1)[1]
            if error_code == str(10):
                raise Exception(f"Disconnected, poorly-connected or mismatched impedance of the antenna")
            elif error_code != str(0):
                raise Exception(f"EC: {error_code}")
    return tags, [bank_number, rf_mode, power]

def hex_to_decimal(hex_value):
    """Convert phase from hexadecimal to decimal."""
    try:
        # Convert hex string to integer
        return int(hex_value, 16)
    except ValueError:
        return float('nan')  # Return NaN for invalid values

def hex_phase_to_degrees(decimal_phase):
    """Convert phase from decimal to degrees."""
    try:
        # Convert to degrees (360 degrees mapped to 4096 values)
        return (decimal_phase * 360.0) / 4096.0
    except (ValueError, TypeError):
        return float('nan')  # Return NaN for invalid values

# Function to handle Ctrl+C and save the DataFrame to CSV
def signal_handler(sig, frame):
    # Convert RSSI and Phase to numeric
    df['RSSI'] = pd.to_numeric(df['RSSI'], errors='coerce')
    df['Phase Decimal'] = pd.to_numeric(df['Phase Decimal'], errors='coerce')
    
    # Calculate averages for each unique distance
    avg_data = df.groupby('Distance [m]').agg({
        'RSSI': 'mean',
        'Phase Decimal': 'mean'
    }).reset_index()
    
    # Round the averages to 2 decimal places
    avg_data['Avg RSSI'] = avg_data['RSSI'].round(2)
    avg_data['Avg Phase Decimal'] = avg_data['Phase Decimal'].round(2)
    
    # Drop the original columns used for calculation
    avg_data = avg_data.drop(['RSSI', 'Phase Decimal'], axis=1)
    
    # Merge the averages back to the original dataframe based on Distance
    final_df = df.merge(avg_data, on='Distance [m]', how='left')
    
    # Sort the dataframe by Distance for better readability
    final_df = final_df.sort_values('Distance [m]')
    
    timestamp = datetime.now().strftime('%d%m%y_%H%M%S')
    filename = f'robot_rfid_data_{timestamp}.csv'
    print(f'\nSaving results to {filename}...')
    
    # Print the averages for each distance
    print("\nAverages for each distance:")
    print(avg_data)
    
    final_df.to_csv(filename, index=False)
    print(f'Results saved to {filename}')
    ser.close()
    sys.exit(0)

def calculate_distance(x, y, z):
    return sqrt(x**2 + y**2 + z**2)

if __name__ == "__main__":
    try:
        ser = serial.Serial('COM3', baudrate=tsl_baudrate, bytesize=tsl_bytesize, 
                          parity=tsl_parity, stopbits=tsl_stopbits, timeout=tsl_timeout)
    except Exception as e:
        print(f"Error opening serial port: {e}")
        exit(1)

    # Initialize antenna and power settings
    antenna = int(input("Please enter the antenna port (1-4): "))
    power = int(input("Please enter the reader power (0-3000): "))
    init(antenna, power)

    # DataFrame to store the results - now including Phase Decimal
    df = pd.DataFrame(columns=['Tag ID', 'RSSI', 'Phase', 'Phase Decimal', 'Antenna', 
                             'Robot X [m]', 'Robot Y [m]', 'Robot Z [m]', 
                             'Robot Rot Z [deg]', 'Distance [m]', 'Note'])

    signal.signal(signal.SIGINT, signal_handler)

    # Ask for the note (optional description)
    note = input("Please enter a note for this measurement session: ")

    while True:
        # Get robot position and rotation (only Z rotation like the second code)
        robot_x = float(input("Please enter the Robot X position [m]: "))
        robot_y = float(input("Please enter the Robot Y position [m]: "))
        robot_z = float(input("Please enter the Robot Z position [m]: "))
        robot_rot_z = float(input("Please enter the Robot Z rotation [deg]: "))

        # Calculate distance from origin
        distance = calculate_distance(robot_x, robot_y, robot_z)

        # Perform inventory
        tag_data = send_command(f'$ba -go'.encode())
        tag_lines = tag_data.split('\n')
        tags, header_bank = extract_tag_details(tag_lines)

        # Add measurements to DataFrame
        for tag in tags:
            # Convert phase to decimal first
            phase_decimal = hex_to_decimal(tag['Phase'])
            
            tag_data = {
                'Tag ID': tag['Tag ID'],
                'RSSI': tag['RSSI'],
                'Phase': tag['Phase'],
                'Phase Decimal': phase_decimal,
                'Antenna': tag['Antenna'],
                'Robot X [m]': robot_x,
                'Robot Y [m]': robot_y,
                'Robot Z [m]': robot_z,
                'Robot Rot Z [deg]': robot_rot_z,
                'Distance [m]': distance,
                'Note': note
            }
            df = df._append(tag_data, ignore_index=True)

        print("\nCurrent measurements:")
        print(pd.DataFrame([tag_data]))
        print(f"\nTotal measurements recorded: {len(df)}")
        
        # Ask user to proceed to the next measurement
        input(f"Current distance from origin: {distance:.2f} meters. Press Enter to continue to the next measurement or Ctrl+C to stop.")