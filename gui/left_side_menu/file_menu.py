from ctypes import pointer, string_at
from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
from gui.canvas.mesh3dplotter import Mesh3DPlotter
import igl
import os


class FileMenu:
    path = ""
    triangleCount = 0

    def __init__(self, master: Frame, plotter:Mesh3DPlotter):
        self.plotter = plotter
        self.mainFrame = Frame(master)
        self.content = Frame(self.mainFrame, width=220,
                             height=180, padx=20, pady=20)

    def onSelectFile(self):
        filename = askopenfilename(
            filetypes=[("Object files", ".obj")])

        if os.path.isfile(filename):
            self.path = filename
            self.fileNameLabel.configure(text=filename.split("/")[-1])
            self.verticesLabel.configure(text="Reading...")
            self.facesLabel.configure(text="Reading...")

            v, self.triangles = igl.read_triangle_mesh(os.path.join(os.getcwd(), filename))
            self.verticesLabel.configure(text=str(len(v)))
            self.facesLabel.configure(text=str(len(self.triangles)))
            self.plotter.plotFile(v, self.triangles, filename)

    def getKeyValueFrame(self, parent: Frame, key: str, valueLength: float = 100):
        keyValFrame = Frame(parent)
        keyLabel = Label(keyValFrame, text=key, width=8,
                         anchor=W, justify=LEFT, wraplength=70)
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text="-", wraplength=valueLength)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel


    def build(self):
        self.content.pack_propagate(0)

        title = Label(self.content, text="Select")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill=BOTH, side=TOP, pady=(0, 10))

        fileSelectionFrame = Frame(self.content)
        chooseFrame = Frame(fileSelectionFrame)

        chooseFile = Label(chooseFrame, text="Choose File", anchor=W)
        chooseFile.configure(font=("Helvetica", 10, "bold"))
        chooseFile.pack(fill=BOTH, side=LEFT)

        button = TkinterCustomButton(master=chooseFrame, text="Select",
                command=self.onSelectFile, corner_radius=60, height=25, width=80)
        button.pack(side=LEFT, padx=5)
        chooseFrame.pack(side=TOP, pady=(0, 10))

        self.fileNameLabel = self.getKeyValueFrame(fileSelectionFrame, "Name")
        self.verticesLabel = self.getKeyValueFrame(fileSelectionFrame, "Vertices")
        self.facesLabel = self.getKeyValueFrame(fileSelectionFrame, "Faces")

        fileSelectionFrame.pack(side=TOP, anchor=W)

        self.content.pack(side="top")
        self.mainFrame.pack(side="top", anchor=N)
