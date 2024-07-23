import cv2, numpy as np
from src.io import StubIO
from src.types import Frame, Point
from src.utils import calculate_euclidean_distance, calculate_xy_distance

stub =StubIO()

class Camera:

    def __init__(self, frame:Frame):
        self.min_distance =5
        self.lk_params =dict(winSize =(15, 15), maxLevel =2, criteria =(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, .03))
        first_frame_as_gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        features_mask =np.zeros_like(first_frame_as_gray)
        features_mask[:, :20] =1
        features_mask[:, :900:1050] =1
        self.features =dict(maxCorners =100, qualityLevel =.3, minDistance =3, blockSize =7, mask =features_mask)

    def get_subject_position_from_camera(self, tracks:dict, camera_movements:list):
        for subject, subject_tracks in tracks.items():
            for frame_id, frame in enumerate(subject_tracks):
                for track_id, track in frame.items():
                    position =track.get('position')
                    if position:
                        camera_movement =camera_movements[frame_id]
                        tracks[subject][frame_id][track_id]['position'] =[position[0] - camera_movement[0], position[1] - camera_movement[1]]

        return tracks

    def estimate_motion(self, frames:list[Frame], read_from_stub =False, stub_path =None):
        print("[+] Detecting camera movements")
        if read_from_stub:
            camera_movements =stub.read(stub_path)
            if camera_movements: return camera_movements

        camera_movements =[[0, 0]] *len(frames)
        prev_frame =cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        prev_features =cv2.goodFeaturesToTrack(prev_frame, **self.features)

        for frame_num in range(1, len(frames)):
            frame =cv2.cvtColor(frames[frame_num], cv2.COLOR_BGR2GRAY)
            features, *_ =cv2.calcOpticalFlowPyrLK(prev_frame, frame, prev_features, None, **self.lk_params)

            max_distance =0
            motion_x, motion_y =0, 0
            for _, (curr, prev) in enumerate(zip(features, prev_features)):
                features_pt =Point(*[int(pt) for pt in curr.ravel()[:2]])
                prev_features_pt =Point(*[int(pt) for pt in prev.ravel()[:2]])

                distance =calculate_euclidean_distance(features_pt, prev_features_pt)
                if distance >max_distance:
                    max_distance =distance
                    motion_x, motion_y =calculate_xy_distance(prev_features_pt, features_pt)

            if max_distance >self.min_distance:
                camera_movements[frame_num] =[motion_x, motion_y]
                prev_features =cv2.goodFeaturesToTrack(frame, **self.features)

            prev_frame =frame.copy()
        if stub_path: stub.write(stub_path, camera_movements)
        return camera_movements