
import os
import time

import cv2

from acq_const import (IMAGE_PATH, FRAME_WIDTH, FRAME_HEIGHT, 
                       I_ENDING, SLEEP_TIME)


def image_recorder(path=IMAGE_PATH, frame_width=FRAME_WIDTH, 
                   frame_height=FRAME_HEIGHT, ending = I_ENDING, 
                   time_between_imag=SLEEP_TIME):
    
    # Initialize camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    # Check whether the camera could be opened
    if not cap.isOpened():
        print('Error: camera could not be opened!')
        exit()

    # Set image resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    image_count = 0

    try:
        while True:
            # Capture image
            ret, frame = cap.read()
        
            if not ret:
                print('Error: frame could not be captured!')
                break
        
            # Save image in JPEG format
            filename = f'image_{image_count}.{ending}'
            filepath = os.path.join(path, filename)
            cv2.imwrite(filepath, frame)
            print(f'Image saved: {filename}')
        
            image_count += 1
            time.sleep(time_between_imag)

    except KeyboardInterrupt:
        print('Recording finished!')

    finally:
        # Close the window / Release webcam
        cap.release()

        # De-allocate any associated memory usage 
        cv2.destroyAllWindows()

        print('Webcam released and memory usage de-allocated!')


if __name__ == '__main__':
    image_recorder(path=IMAGE_PATH, frame_width=FRAME_WIDTH, 
                   frame_height=FRAME_HEIGHT, 
                   time_between_imag=SLEEP_TIME)

