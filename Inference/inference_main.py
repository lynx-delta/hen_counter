 
from object_data_handling import DataHandler


save_to_path = 'path/to/inference'
#source = 'path/to/data/test'  #Video file
source = 0  # Camera
model = 'path/to/trained_model/weights/best.pt'

det_kwargs_dict = {
    'show': False,
    'region': [(0, 240), (640, 240)],
    'model': model,
    'line_width': 2,
    'conf': 0.3,
    'iou': 0.5,
    'device': 0
}

def stream_main(save_to_path=save_to_path, source=source,
                det_kwargs_dict=det_kwargs_dict):
    
    handler = DataHandler()
    handler.process_stream(save_to_path, source_type='video', source=source, 
                           frame_w_h=(640, 480), stride=1, write_to_file=True, 
                           write_video=False, write_interval=10, duration=30,
                           det_kwargs_dict=det_kwargs_dict)
    
def stream_lt_main(save_to_path=save_to_path, source=source,
                   det_kwargs_dict=det_kwargs_dict):
    
    handler = DataHandler()
    handler.process_stream_lt(save_to_path, source=source, 
                              frame_w_h=(640, 480), stride=1, write_to_file=True, 
                              write_interval=30, write_interval_new_f=90, 
                              run_from_to=(9, 19), det_kwargs_dict=det_kwargs_dict)

if __name__ == '__main__':
    stream_lt_main()
    
    