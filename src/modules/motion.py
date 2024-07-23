from src.types import Point
from src.utils import calculate_euclidean_distance

class Motion:

    def __init__(self, fps:int):
        self.frame_window =5
        self.frame_rate =fps
    
    def estimate_subject_motion(self,tracks:dict):
        print("[+] Estimating subject motion")
        total_distance= {}
        for subject, subject_tracks in tracks.items():
            if subject == "ball" or subject == "referees": continue 

            number_of_frames = len(subject_tracks)
            for frame_num in range(0,number_of_frames, self.frame_window):
                last_frame = min(frame_num +self.frame_window, number_of_frames -1)

                for track_id,_ in subject_tracks[frame_num].items():
                    if track_id not in subject_tracks[last_frame]: continue

                    start_position =subject_tracks[frame_num][track_id].get('position_transformed')
                    end_position =subject_tracks[last_frame][track_id].get('position_transformed')
            
                    if start_position is None or end_position is None: continue
                    
                    distance_covered =calculate_euclidean_distance(Point(*[int(pt) for pt in start_position[:2]]), Point(*[int(pt) for pt in end_position[:2]]))
                   
                    time_elapsed = (last_frame-frame_num)/self.frame_rate
                    speed_mps = distance_covered/time_elapsed
                    speed_kph = speed_mps*3.6

                    if subject not in total_distance: total_distance[subject]= {}
                    if track_id not in total_distance[subject]: total_distance[subject][track_id] = 0
                    total_distance[subject][track_id] += distance_covered

                    for frame_num_batch in range(frame_num,last_frame):
                        if track_id not in tracks[subject][frame_num_batch]: continue
                        tracks[subject][frame_num_batch][track_id]['speed'] = speed_kph
                        tracks[subject][frame_num_batch][track_id]['distance'] = total_distance[subject][track_id]