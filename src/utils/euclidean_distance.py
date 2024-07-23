from src.types import Point

def calculate_euclidean_distance(pt1:Point, pt2:Point)->float:
    base =pt1.x -pt2.x
    height =pt1.y -pt2.y
    return (base**2 + height**2) **.5

def calculate_xy_distance(pt1:Point, pt2:Point):
    return pt1.x -pt2.x, pt1.y -pt2.y