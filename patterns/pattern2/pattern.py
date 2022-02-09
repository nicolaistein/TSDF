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

        self.reset()

        self.moveTo(y=(b2-b1)/2)
        self.workHeight()


        self.printTo(x=l1-r)
        self.clockArc(x=l1, y=(b2-b1)/2-r, j=r*-1, arcDegrees=90)
        self.printTo(y=r)
        self.counterClockArc(x=l1+r,y=0, i=r, arcDegrees=90)


        self.printTo(x=l1+l2-r)
        self.counterClockArc(y=r*2, j=r)
        self.printTo(x=l1+l2-l3+r)

        self.clockArc(y=r*4, j=r)
        self.printTo(x=l1+l2-r)

        self.counterClockArc(y=r*6, j=r)
        self.printTo(x=l1+r)


        self.counterClockArc(x=l1, y=b2-r, j=r*-1, arcDegrees=90)
        self.printTo(y=(b2-b1)/2 +b1+r)
        self.clockArc(x=l1-r, y=(b2-b1)/2 +b1, i=r*-1, arcDegrees=90)
        self.printTo(x=0)
        self.freeMoveHeight()

        return "\n".join(self.result), self.commands
