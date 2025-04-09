
import datetime
import json
import os
import time

import cv2
import inspect
import numpy as np
from ultralytics import YOLO

from object_tracking import CustomDetector


class DataHandler():
    '''
    Class for handling object detection data flow

    '''
    
    def __init__(self):

        self.object_detector = None
        self.cap = None
        self.out = None
        self.sleep_state = False

    def init_detector(self, det_kwargs_dict):
        '''
        xxx
        
        '''
        
        self.object_detector = CustomDetector(**det_kwargs_dict)

    def process_stream(self, save_to_path, source_type='cam', source=0, 
                       frame_w_h=(640, 480), stride=1, write_to_file=True, 
                       write_video=False, write_interval=300, duration=1800,
                       det_kwargs_dict={}):
        '''
        xxx
        
        '''

        self.init_detector(det_kwargs_dict)

        try:
            self.cap = cv2.VideoCapture(source)

            # Check whether the camera could be opened
            if not self.cap.isOpened():
                print('Error: camera could not be opened!')
                exit()

            if source_type == 'cam':
                w, h = frame_w_h
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
                fps_raw = self.cap.get(cv2.CAP_PROP_FPS)

            if source_type == 'video':
                w, h, fps_raw = (
                    int(self.cap.get(x)) for x in (
                        cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS
                        )
                    )

            if write_to_file:
                filename_data = self.filename_gen('data')
                write_video = False

            # Process data until 'duration' is reached
            start_time = time.time()
            end_flag = False

            while True:
                counter = 0

                if write_to_file:
                    results, end_flag = self._capture_data(write_interval, counter, 
                                                           stride, end_flag)
                    self._write_to_file(save_to_path, filename_data, results)

                if write_video:
                    end_flag = self._capture_video(save_to_path, write_interval, 
                                                   counter, stride, w, h, fps_raw,
                                                   end_flag)
                
                if (time.time() - start_time >= duration) or end_flag:
                    break
                
        except KeyboardInterrupt as key_int:
            print('Processing iterrupted!')
            
            if inspect.stack()[1].function == 'process_stream_lt':
                raise key_int

        finally:
            # Close the window / Release webcam
            self.cap.release()

            # De-allocate any associated memory usage 
            cv2.destroyAllWindows()

            if write_video:
                self.out.release()

            print('Webcam released and memory usage de-allocated!')

    def process_stream_lt(self, save_to_path, source=0, frame_w_h=(640, 480), 
                          stride=1, write_to_file=True, 
                          write_interval=300, write_interval_new_f=3600, 
                          run_from_to=(9, 19), det_kwargs_dict={}):
        '''
        xxx
        
        '''
        
        try:
            while True:
                t = datetime.datetime.now()

                if (t.hour >= run_from_to[0]) and (t.hour < run_from_to[1]):
                    
                    folder_name = str(datetime.date.today())
                    save_to_path_new = os.path.join(save_to_path, folder_name)

                    if not os.path.exists(save_to_path_new):
                        os.makedirs(save_to_path_new)

                    # Process data until 'write_interval_lt_s' is reached
                    self.process_stream(save_to_path_new, source_type='cam', source=source, 
                                        frame_w_h=frame_w_h, stride=stride, 
                                        write_to_file=write_to_file, 
                                        write_interval=write_interval, 
                                        duration=write_interval_new_f,
                                        det_kwargs_dict=det_kwargs_dict)
                    self.sleep_state = False

                else:
                    if not self.sleep_state:
                        print('...sleeping...')
                        self.sleep_state = True

        except KeyboardInterrupt:
            print('Long-time processing iterrupted!')
    
    @staticmethod
    def filename_gen(file_type):
        '''
        xxx
        
        '''
        
        t = datetime.datetime.now()
        file_name_com = str(datetime.date.today()) + '_' + str(t.hour) + '-' + str(t.minute)

        if file_type == 'data':
            filename = f'data_{file_name_com}.txt'

        if file_type == 'video':
            filename = f'video_{file_name_com}.avi'

        return filename
    
    def _capture_data(self, write_interval, counter, 
                      stride, end_flag):
        '''
        xxx
        
        '''
        
        start_time = time.time()
    
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print('Last frame processed or frame could not be captured!')
                end_flag = True
                break
            
            if counter % stride == 0:
                results = self.object_detector.process(frame, 
                                                       return_format='custom')

            if time.time() - start_time >= write_interval:
                break

            counter += 1

        return results, end_flag
    
    def _write_to_file(self, save_to_path, filename_data, results):
        '''
        xxx
        
        '''
        
        filepath = os.path.join(save_to_path, filename_data)

        try:
            if os.path.exists(filepath):
                mode = 'a'
            else:
                mode = 'w' 
            
            handle = open(filepath, mode)
            json.dump(results, handle)
            handle.write(os.linesep)
        
        except Exception as e:
            print('Writing to file not successful!')
        finally:
            handle.close()

    def _capture_video(self, save_to_path, write_interval, counter, 
                       stride, w, h, fps_raw, end_flag):
        '''
        xxx
        
        '''
        
        fps_w = int(fps_raw / stride)
        filename_video = self.filename_gen('video')
        filepath = os.path.join(save_to_path, filename_video)
        self.out = cv2.VideoWriter(
                        filepath, cv2.VideoWriter_fourcc(*'mp4v'), fps_w, (w, h)
                        )
        
        start_time = time.time()
    
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print('Last frame processed or frame could not be captured!')
                end_flag = True
                break
            
            if counter % stride == 0:
                results = self.object_detector.process(frame, 
                                                       return_format='standard')
                self.out.write(results.plot_im)

            if time.time() - start_time >= write_interval:
                break

            counter += 1

        print(f'Video saved: {filename_video}')
        self.out.release()

        return end_flag





