# id=Simple_2
# author=Nicolai Stein
# params=l1,l2,l3,b1,b2

from patterns.pattern_parent import PatternParent


class Pattern(PatternParent):
    def gcode(self):
        l1 = self.values["l1"]
        l2 = self.values["l2"]
        l3 = self.values["l3"]
        b1 = self.values["b1"]
        b2 = self.values["b2"]
        r = b2 / 6
        printingBetweenArcsNeeded = 4 * r + b1 < b2
        rBottom = r if printingBetweenArcsNeeded else (b2 - b1) / 4
        
        bottom = -(b2-b1)/2
        top = (b2-b1)/2 + b1

        self.reset()
        self.moveTo()

        self.drawPlatformStart()

        self.printTo(x=l1 - rBottom)
        self.clockArc(x=l1, y=-rBottom, j=rBottom * -1, arcDegrees=90)
        if printingBetweenArcsNeeded:
            self.printTo(y= bottom + rBottom)
        self.counterClockArc(x=l1 + rBottom, y=bottom, i=rBottom, arcDegrees=90)

        self.printTo(x=l1 + l2 - r)
        self.counterClockArc(y=bottom + r*2, j=r)
        self.printTo(x=l1 + l2 - l3 + r)

        self.clockArc(y=bottom + r*4, j=r)
        self.printTo(x=l1 + l2 - r)

        self.counterClockArc(y=bottom + r*6, j=r)
        self.printTo(x=l1 + rBottom)

        self.counterClockArc(x=l1, y=top - rBottom, j=rBottom * -1, arcDegrees=90)
        if printingBetweenArcsNeeded:
            self.printTo(y=b1 + rBottom)
        self.clockArc(
            x=l1 - rBottom, y=b1, i=rBottom * -1, arcDegrees=90
        )
        self.printTo(x=0)


        self.drawPlatformEnd()

        self.freeMoveHeight()

        self.onFinish()

        return self.getResult(), self.commands, self.currentE
