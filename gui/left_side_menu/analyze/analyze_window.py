from logger import log
from tkinter import *
from gui.pattern_model import PatternModel
from gui.button import TkinterCustomButton
import gui.left_side_menu.analyze.runtimes as runtimes
import gui.time_formatter as formatter


class AnalyzeWindow:
    def __init__(
        self,
        root,
        vertexCount: int,
        triangleCount: int,
        closed: bool,
        basicShape: bool,
        curves: bool,
    ):
        self.window = Toplevel(root)
        self.window.iconbitmap("image.ico")
        self.closed = closed
        self.basicShape = basicShape
        self.curves = curves
        self.vertexCount = vertexCount
        self.triangleCount = triangleCount

    def abort(self):
        self.buttonCancel.delete()
        self.window.destroy()

    def buildHeading(self, master: Frame, text: str, pady=30):
        label = Label(master, text=text)
        label.configure(font=("Helvetica", 12, "bold"))
        label.pack(side=TOP, anchor=W, pady=(pady, 0))

    def getKeyValueFrame(self, parent: Frame, key: str, value: str):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, anchor=W, justify=LEFT, width=14)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text=value, wraplength=200)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w", pady=(5, 0))
        return valLabel

    def getSuggestion(self):

        if self.basicShape:
            if not self.curves:
                res = "BFF with the amount of cones being the number of visible corners in the mesh."
            else:
                res = "BFF with the amount of cones ideally being the number of visible corners in the mesh + the number of total vertices along the arcs and circles. An approximation should be enough."

        else:
            if self.closed:
                res = "Since the object is closed: Segmentation + ARAP/BFF depending on the quality of the result"

            else:
                res = "ARAP/BFF and if the distortion is too high continue with segmentation"

        return res

    def openWindow(self):
        self.window.title("Analyzation results")
        self.window.resizable(False, False)

        mainContainer = Frame(self.window, padx=20, pady=20)

        self.buildHeading(mainContainer, "Estimated Runtimes", 0)
        self.getKeyValueFrame(
            mainContainer,
            "BFF",
            formatter.formatTime(runtimes.bffTime(self.triangleCount, self.basicShape))
            + " per cone",
        )
        self.getKeyValueFrame(
            mainContainer,
            "LSCM",
            formatter.formatTime(runtimes.lscmTime(self.triangleCount)),
        )
        self.getKeyValueFrame(
            mainContainer,
            "ARAP",
            formatter.formatTime(runtimes.arapTime(self.triangleCount)),
        )
        self.getKeyValueFrame(mainContainer, "Segmentation", "No data available yet")
        self.getKeyValueFrame(mainContainer, "Automatic Mode", "No data available yet")

        self.buildHeading(mainContainer, "Possibilities")

        maxCones = self.vertexCount
        Label(mainContainer, text="BFF with max. " + str(maxCones) + " cones").pack(
            side="top", anchor="w"
        )
        if not self.closed:
            Label(mainContainer, text="LSCM").pack(side="top", anchor="w")
            Label(mainContainer, text="ARAP").pack(side="top", anchor="w")
        Label(mainContainer, text="Segmentation + BFF/ARAP/LSCM").pack(
            side="top", anchor="w"
        )

        self.buildHeading(mainContainer, "Suggestion")
        Label(
            mainContainer, text=self.getSuggestion(), wraplength=250, justify=LEFT
        ).pack(side=TOP, anchor=W)

        # buttons
        buttonFrame = Frame(mainContainer)

        self.buttonCancel = TkinterCustomButton(
            master=buttonFrame,
            text="Close",
            command=self.abort,
            fg_color="#a62828",
            hover_color="#c75454",
            corner_radius=60,
            height=25,
            width=80,
        )
        self.buttonCancel.pack(side=LEFT)

        buttonFrame.pack(side=TOP, anchor=W, pady=(30, 0))

        mainContainer.pack(anchor=NW)
        self.window.mainloop()
