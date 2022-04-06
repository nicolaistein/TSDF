from tkinter import *
from tkinter.filedialog import askopenfilename
from gui.button import TkinterCustomButton
from gui.mesh3dplotter.mesh3dplotter import Mesh3DPlotter
from gui.menu_heading.menu_heading import MenuHeading
import gui.menu_heading.info_texts as infotexts
import igl
import os


class FileMenu:
    triangleCount = 0
    triangles = []
    v = []
    currentObject = ""
    currentChart = ""

    def __init__(self, master: Frame, plotter: Mesh3DPlotter, mainColor: str):
        self.mainColor = mainColor
        self.plotter = plotter
        plotter.notifyFileMenu = self.onChartSelect
        self.mainFrame = Frame(master)
        self.content = Frame(self.mainFrame, width=260, height=200, padx=20, pady=20)

    def onChartSelect(self, chart: int):
        if chart == -1:
            self.currentChart = ""
        else:
            self.currentChart = (
                os.getcwd() + "/algorithms/segmentation/result/" + str(chart) + ".obj"
            )
        self.refreshInfo()

    def refreshInfo(self):
        filename = self.currentObject.split("/")[-1]
        fileText = filename if filename else "-"

        chart = self.currentChart.split("/")[-1]
        chart = chart.split(".")[0]
        chartText = "#" + str(chart) if chart else "-"

        if self.currentObject:
            self.v, self.triangles = igl.read_triangle_mesh(
                os.path.join(
                    os.getcwd(),
                    self.currentChart if self.currentChart else self.currentObject,
                )
            )

        for child in self.list.winfo_children():
            child.destroy()

        self.getKeyValueFrame(self.list, "Name", fileText)
        self.getKeyValueFrame(self.list, "Vertices", str(len(self.v)))
        self.getKeyValueFrame(self.list, "Faces", str(len(self.triangles)))

    def onSelectFile(self):
        obj = askopenfilename(filetypes=[("Object files", ".obj")])

        if os.path.isfile(obj):
            self.currentObject = obj
            self.currentChart = ""
            self.refreshInfo()
            self.plotter.plotFile(self.v, self.triangles)

    def getPath(self):
        return self.currentChart if self.currentChart else self.currentObject

    def getKeyValueFrame(self, parent: Frame, key: str, value: str):
        keyValFrame = Frame(parent)
        keyLabel = Label(
            keyValFrame, text=key, width=8, anchor=W, justify=LEFT, wraplength=70
        )
        keyLabel.configure(font=("Helvetica", 10, "bold"))
        keyLabel.pack(side=LEFT)
        valLabel = Label(keyValFrame, text=value, wraplength=140)
        valLabel.pack(side=LEFT)

        keyValFrame.pack(side="top", anchor="w")
        return valLabel

    def build(self):
        self.content.pack_propagate(False)

        MenuHeading("Select File", infotexts.selectFile).build(self.content)
        #        title = Label(self.content, text="Select File")

        fileSelectionFrame = Frame(self.content)
        chooseFrame = Frame(fileSelectionFrame)

        chooseFile = Label(chooseFrame, text="Choose File", anchor=W)
        chooseFile.configure(font=("Helvetica", 10, "bold"))
        chooseFile.pack(fill=BOTH, side=LEFT)

        button = TkinterCustomButton(
            master=chooseFrame,
            text="Select",
            command=self.onSelectFile,
            corner_radius=60,
            height=25,
            width=80,
        )
        button.pack(side=LEFT, padx=5)
        chooseFrame.pack(side=TOP, pady=(0, 10))

        infoFrame = Frame(fileSelectionFrame)
        self.list = infoFrame
        self.refreshInfo()

        infoFrame.pack(side=TOP, anchor=W)
        fileSelectionFrame.pack(side=TOP, anchor=W)

        self.content.pack(side=TOP)
        self.mainFrame.pack(side=TOP, anchor=N)
