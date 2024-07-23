import pandas as pd
import supervision as sv
from ultralytics import YOLO

from src.io import StubIO
from src.utils import BBox
from src.types import Frame, Point

stub =StubIO()

class Inference:

    def __init__(self, model_path:str):
        
        self.inference_model =YOLO(model_path)
        self.object_tracker =sv.ByteTrack()

    def track_subject_position(self, tracks:dict):
        for subject, subject_tracks in tracks.items():
            for frame_id, frame in enumerate(subject_tracks):
                for track_id, track in frame.items():
                    coords =[int(pt) for pt in track['bbox']]
                    bbox =BBox(Point(*coords[:2]), Point(*coords[2:]))

                    tracks[subject][frame_id][track_id]['position'] =[*(bbox.center.coords if subject =='ball' else bbox.bottom.coords)]

        return tracks
    
    def detect_object(self, frames:list[Frame], batch:int):
        detections =[]
        for i in range(0, len(frames), batch):
            frame_batches =frames[i:i+batch]
            batch_detections =self.inference_model.predict(frame_batches, conf =.1)
            detections +=batch_detections
        return detections
    
    def track_objects(self, frames:list[Frame], infer_from_stub =False, stub_path:str =None, batch =25):
        print("[+] Savana inferencing")
        if infer_from_stub: 
            footprints =stub.read(stub_path)
            if footprints: return self.track_subject_position(footprints)

        footprints ={'players': [], 'referees': [], 'ball': []}
        preds =self.detect_object(frames, batch)
        for frame_id, pred in enumerate(preds):
            object_classes =pred.names
            object_classes_inv ={value:key for key, value in object_classes.items()}

            # cast detections to supervision format
            supervision_detections =sv.Detections.from_ultralytics(pred)

            # a goalkeeper is also a player ;)
            for index, class_id in enumerate(supervision_detections.class_id):
                if object_classes.get(class_id) =='goalkeeper': 
                    supervision_detections.class_id[index] =object_classes_inv.get('player')

            # set object tracks :)
            object_tracks =self.object_tracker.update_with_detections(supervision_detections)

            footprints['ball'].append({})
            footprints['players'].append({})
            footprints['referees'].append({})
            
            for track in object_tracks:
                bbox =track[0].tolist()
                track_id =track[4]
                class_id =track[3]
                if object_classes_inv.get('player') ==class_id: footprints['players'][frame_id][track_id] ={'bbox': bbox}
                if object_classes_inv.get('referee') ==class_id: footprints['referees'][frame_id][track_id] ={'bbox': bbox}
            
            for detection in supervision_detections:
                bbox =detection[0].tolist()
                track_id =detection[4]
                class_id =detection[3]
                if object_classes_inv.get('ball') ==class_id: footprints['ball'][frame_id][1] ={'bbox': bbox}
        if stub_path: stub.write(stub_path, footprints)
        return self.track_subject_position(footprints)

    def interpolate_ball_position(self, ball_positions):

        ball_positions = [x.get(1,{}).get('bbox',[]) for x in ball_positions]
        df_ball_positions = pd.DataFrame(ball_positions,columns=['x1','y1','x2','y2'])

        # Interpolate missing values
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()

        return [{1: {"bbox":x}} for x in df_ball_positions.to_numpy().tolist()]
    