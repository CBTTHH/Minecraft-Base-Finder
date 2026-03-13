
class Detection:
    def __init__(self, type_:str):
        self.type = type_
        self.coords = set()

    def add_coords(self, coord):
        if not isinstance(coord, tuple) or len(coord) != 3:
            raise TypeError("Coord need be a tuple of 3 integers")
        self.coords.add(coord)
    
    def r_amount(self):
        return len(self.coords)
        
    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.r_amount(),
            "coords": list(self.coords)
        }
        
    def merge(self, other: "Detection"):
        if not isinstance(other, Detection):
            raise TypeError("Can only merge with another Detection class")
        if self.type != other.type:
            raise ValueError(f"Cannot merge different detection types: {self.type} and {other.type}")
        
        self.coords.update(other.coords)
    
    def __iadd__(self, other):
        if not isinstance(other, Detection):
            raise TypeError(f"Unsupported argument {type(other)} for += operation. It needs to be a Detection class")
        if self.type != other.type:
            raise ValueError("Cannot merge different detection types")
        
        self.coords.update(other.coords)
        return self
        
    
    
    