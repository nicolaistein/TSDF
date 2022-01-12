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

        self.reset()

        #Move to start point
        self.moveTo()
        
        self.workHeight()
        self.printTo(x=l1-r)


        self.counterClockArc(y=r*2, j=r)
        self.printTo(x=l1-l2+r)

        self.clockArc(y=r*4, j=r)
        self.printTo(x=l1-r)

        self.counterClockArc(y=r*6, j=r)
        self.printTo(x=0)

        self.freeMoveHeight()
    #    self.moveTo(y=0)
    #    print("# ----------------------")
    #    print(self.result)
    #    print("# ----------------------")

        return self.result, self.commands
