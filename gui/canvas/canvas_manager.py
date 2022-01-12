from tkinter import *

from PIL.Image import init
import gui.canvas.translator as translator
from patterns.gcode_cmd import GCodeCmd
from gui.pattern_model import PatternModel

class CanvasManager:

    plotFaces:bool = False
    plotDistortion:str = "none"

    def __init__(self, master: Frame, initSize: int):
        self.placedPatternsMenu = None
        self.master = master
        self.size = initSize
        self.xmax = initSize
        self.ymax = initSize
        self.points = []
        self.faces = []
        self.patterns = {}
        self.flatObjectOnCanvas = []
        self.distortionOnCanvas = []
        self.rulers = []
        self.selectedPattern = None

    def P(self, x,y):
        """
        Transform point from cartesian (x,y) to Canvas (X,Y)
        """
        M=4
        X = M + (x/self.xmax) * (self.size-2*M)
        Y = M + (1-(y/self.ymax)) * (self.size-2*M)
        return (X,Y)

    def plot(self, points, faces, areaDistortions, angularDistortions):
        self.areaDistortions = areaDistortions
        self.angularDistortions = angularDistortions
        self.faces = faces    
        pointsNew = translator.moveToPositiveArea(points)
#        self.scale, self.points = translator.scale(pointsNew, self.size)
        self.points = pointsNew
        maxValue = 0
        for p in pointsNew:
            for x in p:
                if maxValue < x: maxValue = x

        self.xmax = self.ymax = round(maxValue, 2)

        for index, p in enumerate(self.points):
            self.points[index] = list(self.P(p[0], p[1]))


        self.plotDistortion = "none"
        self.plotFaces = False

        self.placedPatternsMenu.deleteAll()
        self.show()

    def selectPattern(self, pattern: PatternModel):
        selected = self.selectedPattern
        if selected is None or not selected == pattern:
            self.selectedPattern = pattern

            if not selected is None:
                self.refreshPattern(selected)
        else:
            self.selectedPattern = None
        self.refreshPattern(pattern)

    def createLine(self, x1, x2):
        self.flatObjectOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1]))

    def plotRulers(self):
        max = self.size - 4
        min = 4
        length = 820

        topLeft = self.size-length
        bottomRight = length
        diff = 10

        l1 = self.canvas.create_line(min, max, min, topLeft)
        l2 =self.canvas.create_line(min, max, length, max)

        l3 =self.canvas.create_line(4, topLeft, min+diff, topLeft+diff)
        l4 =self.canvas.create_line(bottomRight, max, bottomRight-diff, max-diff)

        l5 =self.canvas.create_text(min+20,topLeft-10,fill="darkblue",font=("Purisa", 10), text=str(self.ymax))
        l6 =self.canvas.create_text(bottomRight+25,max-5,fill="darkblue",font=("Purisa", 10), text=str(self.xmax))

        self.rulers.extend([l1, l2, l3, l4, l5, l6])

    def onFaces(self):
        self.plotFaces = not self.plotFaces
        self.clear(True, False, False)
        self.showFlatObject()
        

    def onDistortionPress(self, distortion:str = "none"):
        if self.plotDistortion == distortion: 
            self.plotDistortion = "none"
        else:
            self.plotDistortion = distortion
        self.show()

    def show(self):
        self.clear(True, True)
        self.plotRulers()
        self.showDistortion()
        self.showFlatObject()
        
    def showDistortion(self):
        if self.plotDistortion == "area": self.showAreaDistortion()
        if self.plotDistortion == "angle": self.showAngleDistortion()
            
    def showFlatObject(self):
        if self.plotFaces:
            for face in self.faces:
                x = list(self.points[face[0]-1])
                y = list(self.points[face[1]-1])
                z = list(self.points[face[2]-1])

                #Border
                self.createLine(x, y)
                self.createLine(y, z)
                self.createLine(z, x)

        else:
            for point in self.points:
                x = point[0]
                y = point[1]
                r = 0
                self.flatObjectOnCanvas.append(self.canvas.create_oval(x - r, y - r, x + r, y + r))


    def showAreaDistortion(self):
        for index, face in enumerate(self.faces):
            if index not in self.areaDistortions: continue

            x = list(self.points[face[0]-1])
            y = list(self.points[face[1]-1])
            z = list(self.points[face[2]-1])

            maxDistort = 20
            distortion = self.areaDistortions[index]

            if distortion > 1:
                distFac = distortion
                if distFac > maxDistort:
                    distFac = maxDistort
                if distFac < 1:
                    distFac = 1

                distFac = distFac-1
                distFac = distFac/(maxDistort-1)
                distFac = 1-distFac

                colorFac = int(round(distFac * 255, 0))
                color = '#%02x%02x%02x' % (255, colorFac, colorFac)

            else:
                blueFac = distortion
                colorFac = int(round(blueFac * 255, 0))
                color = '#%02x%02x%02x' % (colorFac, colorFac, 255)
            
            self.distortionOnCanvas.append(
            self.canvas.create_polygon(x, y, z, fill=color))


    def showAngleDistortion(self):
        for index, face in enumerate(self.faces):
            if index not in self.angularDistortions: continue

            x = list(self.points[face[0]-1])
            y = list(self.points[face[1]-1])
            z = list(self.points[face[2]-1])
            
            distortion = self.angularDistortions[index]/30
            if distortion > 1:
                distortion = 1

            distFac = 1-distortion
            colorFac = int(round(distFac * 255, 0))
            color = '#%02x%02x%02x' % (colorFac, 255, colorFac)
            
            self.distortionOnCanvas.append(
                self.canvas.create_polygon(x, y, z, fill=color))



    def build(self):
        canvasFrame = Frame(self.master, height=self.size, width=self.size)
        self.canvas = Canvas(canvasFrame, height=self.size, width=self.size)
        canvasFrame.pack(side=LEFT, anchor=N)
        self.canvas.pack(side=LEFT)
        self.plotRulers()

    def clearList(self, list):
        for point in list:
            self.canvas.delete(point)
        list.clear()

    def clear(self, object:bool, distortion:bool, rulers:bool=True):
        if distortion:
            self.clearList(self.distortionOnCanvas)
        if object:
            self.clearList(self.flatObjectOnCanvas)
        if rulers:
            self.clearList(self.rulers)

    def deletePattern(self, pattern:PatternModel):
        self.removePatternFromCanvas(pattern)
        if self.selectedPattern == pattern:
            self.selectedPattern = None

    def removePatternFromCanvas(self, pattern:PatternModel):
        for shape in self.patterns[pattern]:
            self.canvas.delete(shape)
        self.patterns[pattern] = []


    def refreshPattern(self, pattern:PatternModel):
        self.removePatternFromCanvas(pattern)
        self.addPattern(pattern)

    def addPattern(self, pattern:PatternModel):
        result, commands = pattern.getGcode()
        color = "blue"
        #Change color to red if selected
        if not self.selectedPattern is None:
            color = "red" if self.selectedPattern == pattern else "blue"

        shapes = []
        for cmd in commands:
            s = []
            if(cmd.prefix == "G1"):
                p1x, p1y = self.P(cmd.previousX, cmd.previousY)
                p2x, p2y = self.P(cmd.x, cmd.y)
                s = self.canvas.create_line(p1x,p1y,p2x,p2y, fill=color, width=1)

            if cmd.prefix == "G02" or cmd.prefix == "G03":
                s = self.computeArc(cmd, color)

            shapes.append(s)

        self.patterns[pattern] = shapes

    def computeArc(self, cmd:GCodeCmd, color:str):
        points = [self.P(cmd.previousX, cmd.previousY)]

        cornerPoints = self.getCornerPoints(cmd.prefix=="G02", cmd.arcDegrees, cmd.previousX, cmd.previousY, cmd.x, cmd.y)
        points.append(cornerPoints)

        points.append(self.P(cmd.x, cmd.y))
        return self.canvas.create_line(points, smooth=True, fill=color, width=1)
        

    def getCornerPoints(self, clockwise:bool, degrees:float, x:float, y:float, x2:float, y2:float):
        #Compute orthogonal vector to v2-v vector
        xOrtho = halfY = (y2 - y) / 2
        yOrtho = halfX = (x2 - x) / 2

        if clockwise: xOrtho *= -1
        else: yOrtho *= -1

        if degrees == 180:
            return [self.P(x + xOrtho, y + yOrtho), self.P(x2 + xOrtho, y2 + yOrtho)]
        if degrees == 90:
            return [self.P(x + + halfX + xOrtho, y + halfY + yOrtho)]

