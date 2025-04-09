
from time import time
from datetime import datetime

import numpy as np
from ultralytics.solutions.object_counter import ObjectCounter
from ultralytics.solutions.solutions import BaseSolution, SolutionAnnotator, SolutionResults
from ultralytics.utils.plotting import colors


class CustomDetector(ObjectCounter):
    '''
    Custom class for object detection, object tracking and speed estimation
    
    '''

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.initialize_region() 

        # Speed estimation attributes
        self.spd = {}  # Dictionary for speed data
        self.trkd_ids = []  # List for already speed-estimated and tracked IDs
        self.trk_pt = {}  # Dictionary for tracks' previous timestamps
        self.trk_pp = {}  # Dictionary for tracks' previous positions
    
    def process(self, frame, return_format='custom'):
        '''
        Process input data (frames or object tracks), update object counts,
        and estimate speed

        '''

        self.extract_tracks(frame)  # Extract tracks
        self.annotator = SolutionAnnotator(frame, line_width=self.line_width)  # Initialize annotator

        self.annotator.draw_region(
            reg_pts=self.region, color=(70, 130, 180), thickness=self.line_width * 2
            )  # Draw region

        # Iterate over bounding boxes, track ids and classes index
        for box, track_id, cls in zip(self.boxes, self.track_ids, self.clss):
            # Object counting
            # Draw bounding box and counting region
            self.annotator.box_label(box, label=self.names[cls], color=colors(cls, True))
            self.store_tracking_history(track_id, box)  # Store track history
            self.store_classwise_counts(cls)  # Store classwise counts in dict

            current_centroid = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            # Store previous position of track for object counting
            prev_position = None
            if len(self.track_history[track_id]) > 1:
                prev_position = self.track_history[track_id][-2]
            self.count_objects(current_centroid, track_id, prev_position, cls)  # Perform object counting

            # Speed estimation
            # Initialize tracking data for new objects
            if track_id not in self.trk_pt:
                self.trk_pt[track_id] = 0
            if track_id not in self.trk_pp:
                self.trk_pp[track_id] = self.track_line[-1]

            # Determine if object is crossing the speed estimation region
            if self.LineString([self.trk_pp[track_id], self.track_line[-1]]).intersects(self.r_s):
                direction = 'known'
            else:
                direction = 'unknown'

            # Calculate speed for objects crossing the region for the first time
            if direction == 'known' and track_id not in self.trkd_ids:
                self.trkd_ids.append(track_id)
                time_difference = time() - self.trk_pt[track_id]
                if time_difference > 0:
                    # Calculate speed based on vertical displacement and time
                    self.spd[track_id] = (
                        np.abs(self.track_line[-1][1] - self.trk_pp[track_id][1]) / time_difference
                        ).item()

            # Update tracking data for next frame
            self.trk_pt[track_id] = time()
            self.trk_pp[track_id] = self.track_line[-1]

        plot_im = self.annotator.result()
        self.display_counts(plot_im)  # Display the counts on the frame
        self.display_output(plot_im)  # Display output with base class function

        # Return results
        if return_format == 'custom':
            now = datetime.now()
            speed_data = list(self.spd.values())

            if not speed_data:
                speed_data = [0.0001]

            return {
                'timestamp': str(now.time()),
                'in_count': self.in_count,
                'out_count': self.out_count,
                'classwise_count': self.classwise_counts,
                'speed_max': np.max(speed_data),
                'speed_min': np.min(speed_data),
                'speed_perc_75': np.percentile(speed_data, 75),
                'speed_perc_50': np.percentile(speed_data, 50),
                'speed_mean': np.mean(speed_data)
                }
        
        else:
            return SolutionResults(
            plot_im=plot_im,
            in_count=self.in_count,
            out_count=self.out_count,
            classwise_count=self.classwise_counts,
            total_tracks=len(self.track_ids),
            speed_dict = self.spd
            )

