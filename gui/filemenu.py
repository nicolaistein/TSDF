from ctypes import string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton


class Menu:
    file = "[filename]"

    points = []

    def __init__(self, master: Frame, canvas: Canvas):
        self.leftFrame = Frame(master, height=320, width=260)
        self.canvas = canvas
        self.v = IntVar()
        self.v.set(1)

    def selectFile(self):
        print("Selecting file...")
        filename = askopenfilename(filetypes=[("Object files", ".obj")])
        print("Selected file: ", filename)
        self.file = filename
        self.fileLabel.configure(text=self.file.split("/")[-1])

    def ShowChoice(self):
        print(self.v.get())

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
        self.fileLabel.pack(fill='both', padx=20)

        fileSelectionFrame.pack(side="top", padx=20, pady=40, fill='both')

    def build(self, side: str):
        self.leftFrame.pack_propagate(0)

        self.assembleFileChooserFrame()

    #    TkinterCustomButton(master=self.leftFrame, text="Compute", command=self.compute,
    #                        corner_radius=60, height=25, width=140).pack(side="top", pady=20)

        self.leftFrame.pack(side=side, padx=20, pady=(0, 20))
