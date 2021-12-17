# name=Simple_4
# author=Nicolai Stein
# params=l1,l2,r, u

from patterns.pattern_parent import PatternParent


class Pattern(PatternParent):

    def gcode(self, startX: float, startY: float, workHeight: float):
        l1 = self.values["l1"]
        l2 = self.values["l2"]
        r = self.values["r"]

        self.result = ""
        self.absoluteMode()

        self.moveTo(z=workHeight)
        self.printTo(x=l1)

        self.relativeMode()

        self.counterClockArc(y=r*2, j=r)
        self.printTo(x=l2*-1)

        self.clockArc(y=r*2, j=r)
        self.printTo(x=l2)

        self.counterClockArc(y=r*2, j=r)

        self.absoluteMode()

        self.printTo(x=0)

        return self.result

    def add(self, val: str):
        self.result += val + "\n"
