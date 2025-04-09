
import os
import time

import cv2

from acq_const import (IMAGE_PATH, VIDEO_PATH, 
                       I_ENDING, V_ENDING)


class VideoRecorder():
    '''
    Video recorder class
    
    '''

    def __init__(self, i_path=IMAGE_PATH, v_path=VIDEO_PATH, 
                 i_ending=I_ENDING, v_ending=V_ENDING):
        
        self.i_path = i_path
        self.v_path = v_path
        self.i_ending = i_ending
        self.v_ending = v_ending

    def video_to_frames_main(self, frame_interval=1):
        '''
        Video to frames main
        
        '''
        
        for file in os.listdir(self.v_path):
                if file.endswith(self.v_ending):
                    try:
                        self._video_to_frames(file, frame_interval)
                    except KeyboardInterrupt:
                        print('Video fragmenting interrupted!')
                    finally:
                        print(f'File: {file}')

        print('Processing finished!')
    
    def _video_to_frames(self, file, frame_interval):
        '''
        Video to frames
        
        '''
        
        file_with_path = os.path.join(self.v_path, file)
        cap = cv2.VideoCapture(file_with_path)
        # Check whether the camera could be opened
        if not cap.isOpened():
            print('Error: video could not be opened!')
            exit()

        name, _ = os.path.splitext(file)
        frame_count = 0

        try:
            while True:
                i_filepath = os.path.join(
                    self.i_path, f'{name}_{frame_count}.{self.i_ending}'
                    )
            
                ret, frame = cap.read()

                if not ret:
                    print('No frame to process!')
                    break
                
                if frame_count % frame_interval == 0:
                    cv2.imwrite(i_filepath, frame)

                frame_count += 1

        finally:
            # Close the window / Release webcam
            cap.release()

            # De-allocate any associated memory usage 
            cv2.destroyAllWindows()


if __name__ == '__main__':
    recorder = VideoRecorder(i_path=IMAGE_PATH, v_path=VIDEO_PATH, 
                             i_ending=I_ENDING, v_ending=V_ENDING)
    recorder.video_to_frames_main(frame_interval=10)