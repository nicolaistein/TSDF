# id=Spiral
# author=Nicolai
# params=l1,l2,b1,b2,x,n

import numpy as np
import math
from logger import log

from patterns.pattern_parent import PatternParent


class Pattern(PatternParent):
    def gcode(self):
        l1 = self.l1 = self.values["l1"]
        l2 = self.l2 = self.values["l2"]
        b1 = self.b1 = self.values["b1"]
        b2 = self.b2 = self.values["b2"]
        x = self.x = self.values["x"]
        n = self.n = int(self.values["n"])
        self.vectorLength = 0.5

        rotation = 3  
        self.vectorRotationMatrix = np.array(
            [
                [math.cos(rotation), math.sin(rotation) * -1],
                [math.sin(rotation), math.cos(rotation)],
            ]
        )

        self.reset()
        # Move to start point
        self.moveTo()
        self.moveTo(y=self.b2/2 - self.b1/2)
        self.drawPlatformStart()
        self.printTo(x=self.l1)

        self.counterClockArc(x=l1+l2, y=b2/2-b1/2, i=l2/2, j=b1/2, arcDegrees=180)
        self.printTo(x=self.currentX-x)
        self.clockArc(x=l1+x, y=b2/2-b1/2, i=(l2-2*x)/-2, j=b1/2, arcDegrees=180)
        
        self.printTo(y=b2/2+b1/2)

        top = l1+l2-2*x

#       j = b1/-2
        j = 0

        log("\nNEW DRAWING PROCESS =======================================\n")

        for i in range(0, n):
            log("Forwards i: " + str(i))
            widthCount = 2*i+1 if 2*i+1 >= 0 else 0
            if i % 2 == 0:
                posX = top-(widthCount*x)
                log("PosX: " + str(posX))
                self.clockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/2, j=j, arcDegrees=180)
            else:
                posX = l1+(widthCount*x)
                log("PosX: " + str(posX))
                self.clockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/-2, j=j, arcDegrees=180)

        if n % 2 == 0:
            self.printTo(x=self.currentX-x)
        else:
            self.printTo(x=self.currentX+x)

        for i in range(n, 0, -1):
            log("Backwards i: " + str(i))
            widthCount = i-2 if i-2 >= 0 else 0
            if i % 2 == 0:
                posX = top-(2*widthCount*x)
                log("PosX: " + str(posX))
                self.counterClockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/2, j=j, arcDegrees=180)
            else:
                posX = l1+(2*widthCount*x)
                log("PosX: " + str(posX))
                self.counterClockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/-2, j=j, arcDegrees=180)


    #    self.counterClockArc(y=r * 2, j=r)
    #    self.printTo(x=l1 - l2 + r)

    #    self.clockArc(y=r * 4, j=r)
    #    self.printTo(x=l1 - r)

    #    self.counterClockArc(y=r * 6, j=r)


        self.printTo(y=self.b2/2 + self.b1/2)
        self.printTo(x=0)
        self.drawPlatformEnd()
        self.freeMoveHeight()
        self.onFinish()

        return self.getResult(), self.commands, self.currentE

    def print(self):
        self.currentLocation = [self.l1, self.b2/2 - self.b1/2]
        self.currentVector = [0, -1]

        while(True):
            self.currentLocation -= self.currentVector * self.vectorLength
            self.printTo(x=self.currentLocation[0], y=self.currentLocation[1])
