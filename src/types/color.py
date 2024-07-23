class Color:
    def __init__(self, red:int, green:int, blue: int):
        rgb_value_range =[*range(256)]
        if not red in rgb_value_range or not green in rgb_value_range or not blue in rgb_value_range: 
            raise ValueError('RGB values range between 0-255')
        
        self.red =red
        self.blue =blue
        self.green =green
    
    @property
    def value(self):
        return (self.red, self.green, self.blue)