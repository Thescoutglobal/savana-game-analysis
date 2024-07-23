from src.utils import BBox
from src.types import Point

class BallPossession:

    def __init__(self):
        self.max_ball_offset =40
        self.team_ball_possesion =[]
    
    def get_player_with_ball(self, players_tracks:dict, ball_bbox:list):
        player =-1
        min_dist =float('inf')
        ball_coords =[int(coord) for coord in ball_bbox]
        ball_pos =BBox(Point(*ball_coords[:2]),Point(*ball_coords[2:])).center
        
        for player_id, track in players_tracks.items():
            coords =[int(coord) for coord in track.get('bbox')]
            left_foot_distance =BBox(Point(coords[0], coords[-1]), ball_pos).distance
            right_foot_distance =BBox(Point(coords[2], coords[-1]), ball_pos).distance
            offset =min(left_foot_distance, right_foot_distance)
            if offset <min_dist and offset <self.max_ball_offset:
                min_dist =offset
                player =player_id

            if player !=-1: self.team_ball_possesion.append(track.get('team'))
            else:
                if len(self.team_ball_possesion): self.team_ball_possesion.append(self.team_ball_possesion[-1])
        return player
