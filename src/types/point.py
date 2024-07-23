class Point:
    def __init__(self, x:int, y:int):
        self.x =x
        self.y =y
        
    @property
    def coords(self):
        return self.x, self.y