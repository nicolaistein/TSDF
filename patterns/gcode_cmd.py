
class GCodeCmd:

    def __init__(self, prefix:str, x:float, y:float,
         z:float=None, i:float=None, j:float=None,
          arcDegrees:int=None, previousX:float=0.0, previousY=0.0):
        self.prefix = prefix
        self.x = x
        self.y = y
        self.z = z
        self.i = i
        self.j = j
        self.arcDegrees = arcDegrees
        self.previousX = previousX
        self.previousY = previousY

    def print(self):
        print("GCodeCMD " + self.prefix + ": x=" + str(self.x) + "  y=" + str(self.y)
        + "  prevX=" + str(self.previousX) + "  prevY=" + str(self.previousY))
