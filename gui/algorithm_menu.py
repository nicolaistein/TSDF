from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.plotting.canvas_manager import CanvasManager


class AlgorithmMenu:
    file = "[filename]"

    points = []

    algorithms = [
        ("BFF", 1),
        ("LSCM", 2),
        ("ARAP", 3),
    ]

    def __init__(self, master: Frame, canvasManager: CanvasManager):
        self.mainFrame = Frame(
            master, width=280, height=285, padx=20, pady=20)
        self.canvasManager = canvasManager
        self.v = IntVar()
        self.v.set(1)

    def calculate(self):
        if(self.v.get() == 1):
            coneCount = int(self.bffConeInput.get("1.0", END)[:-1])
            time, self.points = executeBFF(self.file, coneCount)
        if(self.v.get() == 2):
            time, self.points = executeLSCM(self.file)
        if(self.v.get() == 3):
            time, self.points = executeARAP(self.file)

        print("time: " + str(time) + ", points: " + str(len(self.points)))
        self.canvasManager.plot(self.points)

    def selectFile(self):
        filename = askopenfilename(
            filetypes=[("Object files", ".obj")])

        self.file = filename
        self.fileLabel.configure(text=self.file.split("/")[-1])

    def assembleFileChooserFrame(self):
        fileSelectionFrame = Frame(self.mainFrame)
        chooseFrame = Frame(fileSelectionFrame)

        chooseFile = Label(chooseFrame, text="Choose File", anchor=W)
        chooseFile.configure(font=("Helvetica", 11, "bold"))
        chooseFile.pack(fill='both', side=LEFT)

        button = TkinterCustomButton(master=chooseFrame, text="Select",
                                     command=self.selectFile, corner_radius=60, height=25, width=80)
        button.pack(side=LEFT, padx=5)
        chooseFrame.pack(side=TOP)

        self.fileLabel = Label(fileSelectionFrame, text="", anchor=W)
        self.fileLabel.pack(fill='both')

        fileSelectionFrame.pack(side=TOP, anchor=W)

    def build(self):

        title = Label(self.mainFrame, text="Menu")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 20))

        self.mainFrame.pack_propagate(0)
        self.assembleFileChooserFrame()
        self.assembleAlgoChooserFrame()

        TkinterCustomButton(master=self.mainFrame, text="Calculate", command=self.calculate,
                            corner_radius=60, height=25, width=140).pack(side=TOP, pady=(20, 0))

        self.mainFrame.pack(side=TOP)

    def ShowChoice(self):
        print(self.v.get())

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        if not event.char in "1234567890":
            return "break"

    def assembleAlgoChooserFrame(self):
        selectAlgoFrame = Frame(self.mainFrame)
        selectAlgoTitle = Label(selectAlgoFrame,
                                text="Choose Algorithm")

        selectAlgoTitle.configure(font=("Helvetica", 11, "bold"))
        selectAlgoTitle.pack(side=TOP, anchor=W)

        for txt, val in self.algorithms:
            optionFrame = Frame(selectAlgoFrame)
            Radiobutton(optionFrame,
                        text=txt,
                        height=1,
                        wrap=None,
                        variable=self.v,
                        command=self.ShowChoice,
                        value=val).pack(anchor=W, side=LEFT)

            if(txt == "BFF"):
                Label(optionFrame, text="with").pack(side=LEFT, anchor=W)
                self.bffConeInput = Text(optionFrame, height=1, width=3)
                self.bffConeInput.bind('<Return>', self.cancelInput)
                self.bffConeInput.bind('<Tab>', self.cancelInput)
                self.bffConeInput.bind('<BackSpace>', self.allowInput)
                self.bffConeInput.bind('<KeyPress>', self.onKeyPress)
                self.bffConeInput.insert(END, "10")
                self.bffConeInput.pack(side=LEFT, anchor=W, padx=10)
                Label(optionFrame, text="cones").pack(side=LEFT, anchor=W)
            optionFrame.pack(side=TOP, anchor=W)

        selectAlgoFrame.pack(side=TOP, anchor=W, pady=(10, 0))
