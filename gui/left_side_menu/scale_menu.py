from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
from gui.canvas.canvas_manager import CanvasManager


class ScaleMenu:

    def __init__(self, master: Frame, canvasManager: CanvasManager, initSize: int):
        self.mainFrame = Frame(master)
        self.size = initSize
        self.canvasManager = canvasManager
        self.content = Frame(self.mainFrame, width=220,
                             height=150, padx=20, pady=20)

    def setNewSize(self):
        newSize = int(self.sizeInput.get("1.0", END)[:-1])
        self.canvasManager.resize(newSize)
        print("setSize")

    def cancelInput(self, event):
        return "break"

    def allowInput(self, event):
        pass

    def onKeyPress(self, event):
        if not event.char in "1234567890":
            return "break"

    def build(self, side: str):
        self.content.pack_propagate(0)

        chooseFile = Label(self.content, text="Scale")
        chooseFile.configure(font=("Helvetica", 12, "bold"))
        chooseFile.pack(fill='both', side=TOP)

        infoFrame = Frame(self.content)
        keyLabel = Label(infoFrame, text="Current size")
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        Label(infoFrame, text=str(self.size), anchor=W).pack(
            side=LEFT, padx=(5, 0), pady=(1, 0))
        infoFrame.pack(side=TOP, anchor=W, pady=(20, 0))

        setFrame = Frame(self.content)
        self.sizeInput = Text(setFrame, height=1, width=5)
        self.sizeInput.bind('<Return>', self.cancelInput)
        self.sizeInput.bind('<Tab>', self.cancelInput)
        self.sizeInput.bind('<BackSpace>', self.allowInput)
        self.sizeInput.bind('<KeyPress>', self.onKeyPress)
        self.sizeInput.insert(END, str(self.size))
        self.sizeInput.pack(side=LEFT, anchor=W)

        TkinterCustomButton(master=setFrame, text="Set new size", command=self.setNewSize,
                            corner_radius=60, height=25, width=120).pack(side=LEFT, padx=(10, 0))

        setFrame.pack(side=TOP, anchor=W, pady=(10, 0))

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=side, pady=(20, 0), anchor=N)
