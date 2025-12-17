
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as cv
import numpy as np
import sys
import pandas as pd
from datetime import datetime
from collections import defaultdict
import re

def sanitize_sheet_name(sheet_name):
    """
    Sanitize the sheet name to be valid for Excel
    """
    # Replace invalid characters with underscores
    sheet_name = re.sub(r'[\[\]:*?/\\]', '_', sheet_name)
    
    # Excel sheet names must be 31 characters or less
    sheet_name = sheet_name[:31]
    
    # Sheet name cannot be empty or consist only of underscores
    if not sheet_name or sheet_name.strip('_') == '':
        sheet_name = 'Sheet1'
    
    return sheet_name

def read_camera_parameters(filepath='#Intrinsic Camera Matrix-Reman-Lab (mtx).dat'):
    """
    Read camera calibration parameters from a file
    Returns: camera matrix and distortion coefficients
    """
    try:
        inf = open(filepath, 'r')
    except FileNotFoundError:
        print(f"Error: Camera parameters file not found at {filepath}")
        sys.exit(1)

    cmtx = []
    dist = []

    # ignore first line
    line = inf.readline()
    # read camera matrix
    for _ in range(3):
        line = inf.readline().split()
        line = [float(en) for en in line]
        cmtx.append(line)

    # ignore line that says "distortion"
    line = inf.readline()
    # read distortion coefficients
    line = inf.readline().split()
    line = [float(en) for en in line]
    dist.append(line)

    inf.close()
    return np.array(cmtx), np.array(dist)

def get_qr_coords(cmtx, dist, points):
    """
    Calculate QR code coordinates and project axes
    Returns: projected points, rotation vector, and translation vector
    """
    # Define QR code size in millimeters
    qr_size_mm = 120  #  QR code's actual size in mm
    
    # Selected coordinate points for each corner of QR code (scaled to mm)
    qr_edges = np.array([[0, 0, 0],
                        [0, qr_size_mm, 0],
                        [qr_size_mm, qr_size_mm, 0],
                        [qr_size_mm, 0, 0]], dtype='float32').reshape((4,1,3))

    # Determine the orientation of QR code coordinate system
    ret, rvec, tvec = cv.solvePnP(qr_edges, points, cmtx, dist)

    # Define unit axes scaled to mm for better visualization
    axis_length = qr_size_mm  # Length of axis arrows in mm
    unitv_points = np.array([[0, 0, 0],
                            [axis_length, 0, 0],  # X-axis
                            [0, axis_length, 0],  # Y-axis
                            [0, 0, axis_length]], # Z-axis
                            dtype='float32').reshape((4,1,3))
    
    if ret:
        points, jac = cv.projectPoints(unitv_points, rvec, tvec, cmtx, dist)
        return points, rvec, tvec
    return [], [], []

def calculate_camera_position(rvec, tvec):
    """
    Calculate camera position and orientation relative to QR code
    Returns: position coordinates and rotation angles
    """
    # Convert rotation vector to rotation matrix
    rotation_matrix, _ = cv.Rodrigues(rvec)
    
    # Calculate camera position
    camera_position = -rotation_matrix.transpose() @ tvec
    
    # Calculate rotation angles in degrees
    roll = np.arctan2(rotation_matrix[2,1], rotation_matrix[2,2]) * 180 / np.pi
    pitch = np.arctan2(-rotation_matrix[2,0], 
                       np.sqrt(rotation_matrix[2,1]**2 + rotation_matrix[2,2]**2)) * 180 / np.pi
    yaw = np.arctan2(rotation_matrix[1,0], rotation_matrix[0,0]) * 180 / np.pi
    
    return camera_position, (roll, pitch, yaw)

def draw_axis_labels(img, origin, point, label, color):
    """
    Draw axis line with label
    """
    # Draw the axis line
    cv.line(img, origin, point, color, 5)
    
    # Calculate position for label (slightly offset from axis end)
    label_x = point[0] + 10
    label_y = point[1] + 10
    
    # Draw label with white background for better visibility
    label_size = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
    cv.rectangle(img, 
                (label_x - 2, label_y - label_size[1] - 2),
                (label_x + label_size[0] + 2, label_y + 2),
                (255, 255, 255),
                -1)
    cv.putText(img, label, (label_x, label_y), 
              cv.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

def show_axes(cmtx, dist, camera_id=0):
    """
    Main function to display axes overlaid on QR code from camera feed
    """
    cap = cv.VideoCapture(camera_id)
    qr = cv.QRCodeDetector()

    # Dictionary to store positions for each unique QR code
    qr_positions = defaultdict(list)
    qr_mean_positions = defaultdict(dict)
    
    # Variables for calculating mean position
    start_time = cv.getTickCount()
    
    # Create window
    cv.namedWindow('QR Code Tracking')

    # Store last mean values
    last_mean_values = {}

    while True:
        ret, img = cap.read()
        if not ret:
            break

        # Calculate elapsed time
        current_time = cv.getTickCount()
        elapsed_time = (current_time - start_time) / cv.getTickFrequency()

        # First detect QR code corners (better angle tolerance)
        ret_qr, points = qr.detect(img)

        if ret_qr:
            # If detection successful, try to decode
            text, bbox, _ = qr.detectAndDecode(img)
            
            if text:  # Only process if QR code content was successfully decoded
                points = points.reshape((4, 2))
                axis_points, rvec, tvec = get_qr_coords(cmtx, dist, points)

                if len(axis_points) > 0:
                    # Calculate camera position and orientation
                    camera_position, (roll, pitch, yaw) = calculate_camera_position(rvec, tvec)
                    
                    # Convert position from mm to cm
                    camera_position = camera_position / 10.0
                    
                    # Add current position to buffer for this QR code
                    qr_positions[text].append({
                        'timestamp': datetime.now(),
                        'position': [
                            camera_position[0][0],
                            camera_position[1][0],
                            camera_position[2][0]
                        ],
                        'rotation': [roll, pitch, yaw]
                    })

                    # Draw axes with labels
                    axis_points = axis_points.reshape((4,2))
                    origin = (int(axis_points[0][0]), int(axis_points[0][1]))
                    
                    # Define colors and labels for axes
                    axes_info = [
                        ('X', (0, 0, 255)),  # X-axis (Red)
                        ('Y', (0, 255, 0)),  # Y-axis (Green)
                        ('Z', (255, 0, 0))   # Z-axis (Blue)
                    ]

                    # Draw each axis with label
                    for (label, color), point in zip(axes_info, axis_points[1:]):
                        point = (int(point[0]), int(point[1]))
                        if (origin[0] > 5*img.shape[1] or origin[1] > 5*img.shape[1] or
                            point[0] > 5*img.shape[1] or point[1] > 5*img.shape[1]):
                            continue
                        draw_axis_labels(img, origin, point, label, color)

                    # Display QR code content and current position
                    qr_text = f"QR Content: {text}"
                    pos_text = f"Position (cm): X:{camera_position[0][0]:.2f} Y:{camera_position[1][0]:.2f} Z:{camera_position[2][0]:.2f}"
                    rot_text = f"Rotation (deg): Roll:{roll:.1f} Pitch:{pitch:.1f} Yaw:{yaw:.1f}"
                    
                    y_offset = 30
                    cv.putText(img, qr_text, (10, y_offset), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv.putText(img, pos_text, (10, y_offset + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv.putText(img, rot_text, (10, y_offset + 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    # Calculate and update mean position every 5 seconds
                    if elapsed_time >= 5.0:
                        if qr_positions[text]:
                            recent_positions = [p['position'] for p in qr_positions[text]]
                            mean_pos = np.mean(recent_positions, axis=0)
                            last_mean_values[text] = mean_pos
                            
                            qr_mean_positions[text][datetime.now()] = {
                                'X_Position_cm': mean_pos[0],
                                'Y_Position_cm': mean_pos[1],
                                'Z_Position_cm': mean_pos[2],
                                'QR_Content': text
                            }
                        
                        # Reset timer and clear position buffers
                        start_time = current_time
                        qr_positions.clear()

                    # Display the last mean values if available for this QR code
                    if text in last_mean_values:
                        mean_pos = last_mean_values[text]
                        mean_text = f"Mean (cm): X:{mean_pos[0]:.2f} Y:{mean_pos[1]:.2f} Z:{mean_pos[2]:.2f}"
                        cv.putText(img, mean_text, (10, y_offset + 90), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv.imshow('QR Code Tracking', img)

        # Exit on ESC key
        if cv.waitKey(1) & 0xFF == 27:
            break

    # Save all mean positions to Excel file
    if qr_mean_positions:
        # Convert the nested dictionary structure to a list of records
        excel_data = []
        for qr_content, timestamps in qr_mean_positions.items():
            for timestamp, data in timestamps.items():
                excel_data.append({
                    'Date': timestamp.strftime('%Y-%m-%d'),
                    'Time': timestamp.strftime('%H:%M:%S'),
                    'QR_Content': qr_content,
                    'X_Position_cm': data['X_Position_cm'],
                    'Y_Position_cm': data['Y_Position_cm'],
                    'Z_Position_cm': data['Z_Position_cm']
                })
        
        # Create DataFrame and save to Excel
        df = pd.DataFrame(excel_data)
        excel_filename = f'qr_positions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        
        # Create Excel writer object with xlsxwriter engine
        with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
            # Write all data to first sheet
            df.to_excel(writer, sheet_name='All_Data', index=False)
            
            # Create separate sheets for each QR code
            for qr_content in df['QR_Content'].unique():
                qr_data = df[df['QR_Content'] == qr_content]
                sheet_name = sanitize_sheet_name(qr_content)
                qr_data.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"QR code positions saved to {excel_filename}")

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    # Read camera parameters
    camera_matrix, dist_coeffs = read_camera_parameters()
    
    # Use camera ID 1 (or change as needed)
    camera_id = 0
    if len(sys.argv) > 1:
        camera_id = int(sys.argv[1])
    
    show_axes(camera_matrix, dist_coeffs, camera_id)