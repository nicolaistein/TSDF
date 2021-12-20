from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
import algorithms.translator as translator


class AlgorithmMenu:
    file = "[filename]"

    points = []

    algorithms = [
        ("BFF", 1),
        ("LSCM", 2),
        ("ARAP", 3),
    ]

    def __init__(self, master: Frame, canvas: Canvas):
        self.leftFrame = Frame(master, width=300, height=400, bg="green")
        self.canvas = canvas
        self.v = IntVar()
        self.v.set(1)

    def calculate(self):
        if(self.v.get() == 1):
            time, self.points = executeBFF(self.file, 10)
        if(self.v.get() == 2):
            time, self.points = executeLSCM(self.file)
        if(self.v.get() == 3):
            time, self.points = executeARAP(self.file)

        print("time: " + str(time) + ", points: " + str(len(self.points)))
        self.points = translator.moveToPositiveArea(self.points)
        scale, self.points = translator.scale(self.points, 900)
        self.plot()

    def plot(self):
        self.canvas.delete("all")
        for point in self.points:
            x = point[0]
            y = point[1]
            r = 1
            self.canvas.create_oval(x - r, y - r, x + r, y + r)

    def selectFile(self):
        filename = askopenfilename(
            filetypes=[("Object files", ".obj")])

        self.file = filename
        self.fileLabel.configure(text=self.file.split("/")[-1])

    def assembleFileChooserFrame(self):
        fileSelectionFrame = Frame(self.leftFrame, width=200)
        chooseFrame = Frame(fileSelectionFrame)

        chooseFile = Label(chooseFrame, text="Choose File", anchor=W)
        chooseFile.configure(font=("Helvetica", 12, "bold"))
        chooseFile.pack(fill='both', side="left")

        button = TkinterCustomButton(master=chooseFrame, text="Select",
                                     command=self.selectFile, corner_radius=60, height=25, width=80)
        button.pack(side="left", padx=5)
        chooseFrame.pack(side="top")

        self.fileLabel = Label(fileSelectionFrame, text="", anchor=W)
        self.fileLabel.pack(fill='both')

        fileSelectionFrame.pack(side="top", padx=20, pady=20, anchor=W)

    def build(self):

        self.leftFrame.pack_propagate(0)
        self.assembleFileChooserFrame()
        self.assembleAlgoChooserFrame()

        TkinterCustomButton(master=self.leftFrame, text="Calculate", command=self.calculate,
                            corner_radius=60, height=25, width=140).pack(side="top", pady=20)

        self.leftFrame.pack(side=TOP)

    def ShowChoice(self):
        print(self.v.get())

    def assembleAlgoChooserFrame(self):
        selectAlgoFrame = Frame(self.leftFrame, bg="red")
        selectAlgoTitle = Label(selectAlgoFrame,
                                text="Choose Algorithm          ",
                                justify=LEFT,
                                padx=20)

        selectAlgoTitle.configure(font=("Helvetica", 12, "bold"))
        selectAlgoTitle.pack()

        for txt, val in self.algorithms:
            optionFrame = Frame(selectAlgoFrame, bg="blue")
            Radiobutton(optionFrame,
                        text=txt,
                        height=1,
                        wrap=None,
                        variable=self.v,
                        command=self.ShowChoice,
                        value=val).pack(anchor=W, side="left",
                                        padx=(20, 20),)

            if(txt == "BFF"):
                Label(optionFrame, text="with").pack(side=LEFT, anchor=W)
                self.bffConeInput = Text(optionFrame, height=1, width=3)
                self.bffConeInput.insert(END, "10")
                self.bffConeInput.pack(side=LEFT, anchor=W, padx=10)
                Label(optionFrame, text="cones").pack(side=LEFT, anchor=W)
            optionFrame.pack(side=TOP, anchor=W)

        selectAlgoFrame.pack(side=TOP)
