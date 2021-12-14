from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton


class Menu:
    file = "[filename]"

    points = []

    def __init__(self, master: Frame, canvas: Canvas):
        self.leftFrame = Frame(master, width=260)
        self.canvas = canvas

    def plot(self):
        if(self.file != "[filename]"):
            file = open(self.file, "r")
            for line in file:
                split = line.split(" ")
                self.points.append([float(split[0]), float(split[1])])

            for point in self.points:
                x = point[0]
                y = point[1]
                r = 1
                self.canvas.create_oval(x - r, y - r, x + r, y + r)

    def selectFile(self):
        print("Selecting file...")
        filename = askopenfilename(filetypes=[("SuPa framework files", ".supa")])

        print("Selected file: ", filename)
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

    def build(self, side: str):

        self.assembleFileChooserFrame()

        TkinterCustomButton(master=self.leftFrame, text="Auto plot", command=self.plot,
                            corner_radius=60, height=25, width=140).pack(side="top", pady=20)

        self.leftFrame.pack(side=side, padx=(0, 20))
