
import os
import time

import cv2

from acq_const import (VIDEO_PATH, FRAME_WIDTH, FRAME_HEIGHT, 
                       FRAME_RATE, VIDEO_CODEC, V_ENDING,
                       V_DURATION, SLEEP_TIME)


class VideoRecorder():
    '''
    Video recorder class
    
    '''

    def __init__(self, path=VIDEO_PATH, frame_width=FRAME_WIDTH, 
                 frame_height=FRAME_HEIGHT, fps=FRAME_RATE, 
                 codec=VIDEO_CODEC, ending=V_ENDING, 
                 duration=V_DURATION, time_between_vid=SLEEP_TIME):
        
        self.path = path
        self.frame_width = frame_width 
        self.frame_height = frame_height 
        self.fps = fps 
        self.codec = codec
        self.ending = ending
        self.duration = duration
        self.time_between_vid = time_between_vid
        self.cap = cv2.VideoCapture(0)

        # Check whether the camera could be opened
        if not self.cap.isOpened():
            print('Error: camera could not be opened!')
            exit()
        
        # Set image resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        print(f'Frames per second: {self.cap.get(cv2.CAP_PROP_FPS)}')
    
    def show_live_stream(self):
        '''
        Live stream
        
        '''
        
        try:
            while True:
                ret, frame = self.cap.read()

                if not ret:
                    print('Error: frame could not be captured!')
                    break
                
                cv2.imshow('Live Stream', frame)
                
                # Esc to quit
                if cv2.waitKey(1) == 27: 
                    break

        finally:
            # Close the window / Release webcam
            self.cap.release()

            # De-allocate any associated memory usage 
            cv2.destroyAllWindows()

            print('Webcam released and memory usage de-allocated!')

    def record_main(self):
        '''
        Video recorder main
        
        '''

        # Initialize the counter
        video_count = 0

        # FourCC codec
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        
        try:
            while True:
                filename = f'video_{video_count}.{self.ending}'
                self._record(filename, fourcc)
                video_count += 1
                time.sleep(self.time_between_vid)
                
        except KeyboardInterrupt:
            print('Recording finished!')

        finally:
            # Close the window / Release webcam
            self.cap.release()

            # De-allocate any associated memory usage 
            cv2.destroyAllWindows()

            print('Webcam released and memory usage de-allocated!')
    
    def _record(self, filename, fourcc):
        '''
        Video recorder
        
        '''

        # Create VideoWriter object
        filepath = os.path.join(self.path, filename)
        out = cv2.VideoWriter(filepath, fourcc, self.fps, 
                              (self.frame_width, self.frame_height))
        
        start_time = time.time()
    
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print('Error: frame could not be captured!')
                break
            
            out.write(frame)

            if time.time() - start_time > self.duration:
                break

        print(f'Video saved: {filename}')
        out.release()

 
if __name__ == '__main__':
    recorder = VideoRecorder(path=VIDEO_PATH, frame_width=FRAME_WIDTH, 
                             frame_height=FRAME_HEIGHT, fps=FRAME_RATE, 
                             codec=VIDEO_CODEC, ending=V_ENDING, 
                             duration=V_DURATION, time_between_vid=SLEEP_TIME)
    recorder.record_main()
    #recorder.show_live_stream()