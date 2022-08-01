# id=Spiral
# author=Nicolai
# params=l,b,s,x,n

from patterns.pattern_parent import PatternParent


class Pattern(PatternParent):
    def gcode(self):
        l = self.values["l"]
        b = self.values["b"]
        s = self.values["s"]
        x = self.values["x"]
        n = int(self.values["n"])

        self.reset()
        # Move to start point
        self.moveTo()
        #self.moveTo(y=s/2 - b/2)
        self.drawPlatformStart()
        self.printTo(x=l)

        self.counterClockArc(x=l+s, y=b/2, i=s/2, j=b/2, arcDegrees=180)
        self.printTo(x=self.currentX-x)
        self.clockArc(x=l+x, y=b/2, i=(s-2*x)/-2, arcDegrees=180)
        

        top = l+s-2*x
        j = 0

        for i in range(0, n):
            widthCount = i+1 if i+1 >= 0 else 0
            if i % 2 == 0:
                posX = top-(widthCount*x)
                self.clockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/2, j=j, arcDegrees=180)
            else:
                posX = l+((widthCount+1)*x)
                self.clockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/-2, j=j, arcDegrees=180)

        if n % 2 == 0:
            self.printTo(x=self.currentX-x)
        else:
            self.printTo(x=self.currentX+x)

        for i in range(n, 0, -1):
            widthCount = i-2 if i-2 >= 0 else 0
            if i % 2 == 0:
                posX = top-(widthCount*x)
                self.counterClockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/2, j=j, arcDegrees=180)
            else:
                if i==1: widthCount -= 1
                posX = l+((widthCount+1)*x)

                if i==1:
                    self.counterClockArc(x=posX, y=b, i=abs(posX-self.currentX)/-2, j=j, arcDegrees=180)
                else:
                    self.counterClockArc(x=posX, y=self.currentY, i=abs(posX-self.currentX)/-2, j=j, arcDegrees=180)


        self.printTo(x=0)
        self.drawPlatformEnd()
        self.freeMoveHeight()
        self.onFinish()

        return self.getResult(), self.commands, self.currentE

