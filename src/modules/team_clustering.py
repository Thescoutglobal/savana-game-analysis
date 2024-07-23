import numpy as np
from src.types import Frame, Point
from src.utils import BBox, Clustering

class TeamClustering:
    
    def __init__(self):

        self.engine =Clustering() 
        self.team_colors ={}
        self.team_players ={}

    def get_player_color(self, frame:Frame, bbox:BBox):
        image =frame[bbox.pt1.y:bbox.pt2.y, bbox.pt1.x:bbox.pt2.x]
        player_jersy =image[:int(image.shape[0]/2),:]
        return self.engine.get_subject_color(player_jersy)
    
    def set_team_color(self, frame:Frame, tracks:dict):
        player_colors =[]
        for _, track in tracks.items():
            coords =[int(t) for t in track.get('bbox')]
            bbox =BBox(Point(*coords[:2]), Point(*coords[2:]))
            player_colors.append(self.get_player_color(frame, bbox).value)

        team_colors, self.kmeans =self.engine.cluster_colors(player_colors)
        
        self.team_colors ={i+1: color for i, color in enumerate(team_colors)}

    def get_player_team(self, frame:Frame, bbox:BBox, player_id:int):
        if self.team_players.get(player_id): return self.team_players.get(player_id)
        coords =[int(t) for t in bbox]
        bbox =BBox(Point(*coords[:2]), Point(*coords[2:]))
        player_color =self.get_player_color(frame, bbox)
        team_id =self.kmeans.predict(np.array([*player_color.value]).reshape(1, -1))[0] +1
        self.team_players[player_id] =team_id
        return team_id