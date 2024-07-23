import cv2, numpy as np
from src.utils import BBox
from src.types import Frame, Point, Color

class Annotation:

    def __init__(self, frames:list[Frame], tracks:dict, team_possessions:list[int], *, camera_movements:list[list[int]] =None):
        self.frames =frames
        self.tracks =tracks
        self.team_possessions =team_possessions
        self.camera_movements =camera_movements

    def annotate_objects(self):
        annotations =[]
        players_tracking =self.tracks.get('players')
        referees_tracking =self.tracks.get('referees')
        ball_tracking =self.tracks.get('ball')
        if players_tracking and referees_tracking:
            print("[+] Annotating")
            for frame_id, frame in enumerate(self.frames):
                frame =frame.copy()
                if self.camera_movements: frame =self.draw_camera_motions(frame, frame_id)
                # annotate players
                for track_id, player in players_tracking[frame_id].items():
                    color =Color(*[int(c) for c in player.get('team_color', (0, 0, 255))])
                    coords =[int(pt) for pt in player.get('bbox')]
                    frame =self.draw_ellipse(frame, BBox(Point(*coords[:2]), Point(*coords[2:])), color)
                    frame =self.draw_badge(frame, BBox(Point(*coords[:2]), Point(*coords[2:])), track_id, 'Player', color=color)
                    if player.get('has_ball', False): 
                        frame =self.draw_triangle(frame, BBox(Point(*coords[:2]), Point(*coords[2:])), color=Color(0, 0, 255))
                    frame =self.draw_player_motion(frame, frame_id, players_tracking)

                # annotate referees
                for _, referee in referees_tracking[frame_id].items():
                    coords =[int(pt) for pt in referee['bbox']]
                    frame =self.draw_ellipse(frame, BBox(Point(*coords[:2]), Point(*coords[2:])), color=Color(0, 255, 255))
                
                # annotate ball
                for _, ball in ball_tracking[frame_id].items():
                    coords =[int(pt) for pt in ball['bbox']]
                    frame =self.draw_triangle(frame, BBox(Point(*coords[:2]), Point(*coords[2:])))
                frame =self.draw_possesion_banner(frame, frame_id)
                annotations.append(frame)
        
        return annotations

    def draw_ellipse(self, frame:Frame, bbox:BBox, color:Color, *, thickness =2, lineType =cv2.LINE_4):
        width =bbox.width
        center =(bbox.center.x, bbox.pt2.y)
        cv2.ellipse(frame, center=center, axes=(width, int(.35*width)), angle=.0, startAngle=-45., endAngle=235., color=color.value, thickness=thickness, lineType=lineType)
        return frame
    
    def draw_camera_motions(self, frame:Frame, frame_id:int):
        frame =frame.copy()
        overlay =frame.copy()
        cv2.rectangle(overlay, (0,0), (500, 100),(255, 255, 255), -1)
        alpha =.6
        cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)
        motion_x, motion_y =self.camera_movements[frame_id]
        frame =cv2.putText(frame, f"Camera Movement X: {motion_x:.1f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        frame =cv2.putText(frame, f"Camera Movement Y:  {motion_y:.1f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        return frame
    
    def draw_badge(self, frame:Frame, bbox:BBox, track_id:int, label:int, *, thickness =-1, text_color =Color(0, 0, 0), font_scale =.6, font_weight =2, color =Color(0, 255, 0), width =40, height =20, offset =15):
        if not track_id: return
        center =bbox.center.x
        pt1 =Point(center -width //2, bbox.pt2.y -height//2 +offset)
        pt2 =Point(center +width //2, bbox.pt2.y +height//2 +offset)
        frame =cv2.rectangle(frame, pt1 =pt1.coords, pt2 =pt2.coords, color=color.value, thickness=thickness)

        text_pos =Point(pt1.x+20 if pt1.x <100 else pt1.x +10, (pt1.y +17))
        frame =cv2.putText(frame, str(track_id), org=text_pos.coords, fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=text_color.value, fontScale=font_scale, thickness=font_weight)
        return frame

    def draw_triangle(self, frame:Frame, bbox:BBox, color =Color(0, 255, 0)):
        y =bbox.pt1.y
        x =bbox.center.x
        vertices =np.array([[x, y], [x -10, y -20], [x +10, y -20]])
        cv2.drawContours(frame, [vertices], 0, color.value, cv2.FILLED)
        cv2.drawContours(frame, [vertices], 0, Color(0, 0, 0).value, 2)
        return frame
    
    def draw_possesion_banner(self, frame:Frame, frame_id:int):
        overlay =frame.copy()
        height, width, _ = frame.shape
        rect_width = 800
        rect_height = 100

        top_left = (int((width - rect_width) / 2), int(height - rect_height - 20))
        bottom_right = (int((width + rect_width) / 2), int(height - 20))
        cv2.rectangle(overlay, top_left, bottom_right, (255, 255, 255), -1)
        alpha =.4
        frame =cv2.addWeighted(overlay, alpha, frame, 1 -alpha, 0, frame)
        ball_possessions =np.array(self.team_possessions[:frame_id+1])
        team_1_possession =ball_possessions[ball_possessions ==1].shape[0]
        team_2_possession =ball_possessions[ball_possessions ==2].shape[0]
        team_1 =(team_1_possession/(team_1_possession +team_2_possession)) *100
        team_2 =(team_2_possession/(team_1_possession +team_2_possession)) *100
        frame =cv2.putText(frame, f"Team 1 Ball Possession: {round(team_1)}%", (top_left[0]+100, top_left[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        frame =cv2.putText(frame, f"Team 2 Ball Possession:  {round(team_2)}%", (top_left[0]+100, top_left[1]+80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        return frame
    
    def draw_text(self, track =True):
        pass

    def draw_spotlight(self, track =True):
        pass

    def draw_linking(self, track =True, fill =True):
        pass

    def draw_player_motion(self, frame:Frame, frame_id:int, player_tracks:list):
        for _, track_info in player_tracks[frame_id].items():
            if "speed" in track_info:
                speed = track_info.get('speed',None)
                distance = track_info.get('distance',None)
                if speed is None or distance is None: continue
                coords =[int(pt) for pt in track_info['bbox']]
                position =list(BBox(Point(*coords[:2]), Point(*coords[2:])).bottom.coords)
                position[1] +=40

                position = tuple(map(int,position))
                frame =cv2.putText(frame, f"{speed:.2f} km/h",position,cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
                frame =cv2.putText(frame, f"{distance:.2f} m",(position[0],position[1]+20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
        
        return frame