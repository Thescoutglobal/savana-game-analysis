import cv2, numpy as np

class Field:

    def __init__(self, width =68, length =23.2):
        self.width =width
        self.length =length

        self.camera_view =np.array([[110, 1035], [265, 275], [910, 260], [1640, 916]]).astype(np.float32)
        self.actual_view =np.array([[0, width], [0, 0], [length, 0], [length, width]]).astype(np.float32)
        self.perspective =cv2.getPerspectiveTransform(self.camera_view, self.actual_view)
    
    def tranform_camera_view(self, tracks:dict):
        print("[+] Transforming camera view")
        count =0
        for subject, subject_tracks in tracks.items():
            for frame_id, frame in enumerate(subject_tracks):
                for track_id, track in frame.items():
                    position =track.get('position')
                    if position:
                        position =np.array(position)
                        transformed_position =self.transform_point(position)
                        if transformed_position is not None:
                            transformed_position =transformed_position.squeeze().tolist()
                        tracks[subject][frame_id][track_id]['position_transformed'] =transformed_position  
        return tracks
    
    def transform_point(self, point:np.ndarray):
        pt =(int(point[0]), int(point[1]))
        if not cv2.pointPolygonTest(self.camera_view, pt, False) >=0: return
        point =point.reshape(-1, 1, 2).astype(np.float32)
        point =cv2.perspectiveTransform(point, self.perspective)
        return point.reshape(-1, 2)