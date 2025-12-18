
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import time

if __name__ == "__main__":
    # Open the webcam
    vidcap = cv2.VideoCapture(0)

    if not vidcap.isOpened():
        print("Error: Could not open camera.")
        exit()

    count = 0
    while os.path.exists(f"captured_image_{count}.jpg"):
        count += 1  # Find the next available filename

    print("You have 10 seconds to get ready. Press SPACE to capture during this time.")

    start_time = time.time()  # Start the timer
    captured = False

    while True:
        success, frame = vidcap.read()
        if not success:
            print("Error: Could not capture image.")
            break

        # Display the live feed
        cv2.imshow("Webcam", frame)

        # Wait for the spacebar to capture or check if 10 seconds have passed
        key = cv2.waitKey(1) & 0xFF

        # If spacebar is pressed, capture the image and save
        if key == 32:  # SPACEBAR to capture and save
            filename = f"captured_image_{count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Image saved: {filename}")
            count += 1  # Increment counter
            captured = True  # Image is captured
            break  # Exit after capturing

        # If 10 seconds pass without pressing spacebar, exit
        if time.time() - start_time > 10:
            if not captured:
                print("Time's up! No image captured.")
            break

    vidcap.release()
    cv2.destroyAllWindows()






