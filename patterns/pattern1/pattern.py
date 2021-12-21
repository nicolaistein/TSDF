# id=Simple_1
# author=Nicolai
# params=l1,l2,b

from patterns.pattern_parent import PatternParent


class Pattern(PatternParent):

    def gcode(self):
        l1 = self.values["l1"]
        l2 = self.values["l2"]
        b = self.values["b"]
        r = b/6

        self.result = ""
        self.absoluteMode()

        #Move to start point
        self.moveTo()
        self.moveTo(z=self.workHeight)
        self.printTo(x=l1-r)


        self.counterClockArc(y=r*2, j=r)
        self.printTo(x=l1-l2+r)

        self.clockArc(y=r*4, j=r)
        self.printTo(x=l1-r)

        self.counterClockArc(y=r*6, j=r)
        self.printTo(x=0)

        self.moveTo(z=self.freeMoveHeight)
    #    self.moveTo(y=0)
        print("# ----------------------")
        print(self.result)
        print("# ----------------------")

        return self.result

    def add(self, val: str):
        self.result += val + "\n"

#Pattern(values={"l1": 33, "l2": 10, "b":12}, workHeight=2.8, freeMoveHeight=30, startX=10, startY=10, rotation=-160).gcode()