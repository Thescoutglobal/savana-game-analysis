from src.types import Point
from src.utils.euclidean_distance import calculate_euclidean_distance

class BBox:

    def __init__(self, pt1: Point, pt2: Point):
        self.pt1 =pt1
        self.pt2 =pt2
    
    @property
    def points(self):
        return self.pt1.coords, self.pt2.coords
    
    @property
    def width(self):
        return self.pt2.x - self.pt1.x
    
    @property
    def height(self):
        return self.pt2.y - self.pt1.y
    
    @property
    def center(self):
        x1, y1 =self.pt1.coords
        x2, y2 =self.pt2.coords
        return Point((x1+x2)//2, (y1+y2)//2)
    
    @property
    def distance(self):
        return calculate_euclidean_distance(self.pt1, self.pt2)
    
    @property
    def bottom(self):
        return Point(self.pt1.x +self.pt2.x, self.pt2.y)