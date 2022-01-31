from tkinter import *
from functools import partial
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
from gui.button import TkinterCustomButton
from algorithms.segmentation.plotter import plotFaceColors, distinctColors
from algorithms.segmentation.segmentation import Segmenter
from gui.listview import ListView
from logger import log


class Mesh3DPlotter:

    def __init__(self, master: Frame):
        self.mainFrame = Frame(master, width=360, height=480)
        self.fig = plt.figure()
        self.buttons = []
        self.faces = []
        self.chartList = []
        self.vertices = []
        self.faceColors = []
        self.charts = []
        self.selectedChart = -1
        self.showEdges = False

    def isSegmented(self): return len(self.chartList) != 0

    def viewBrowser(self):
        plotFaceColors(self.vertices, self.faces, self.faceColors)

    def changeEdgeView(self):
        self.showEdges = not self.showEdges
        self.show()

    def build(self):
        self.plotContainer = Frame(self.mainFrame, width=360, height=360)
        self.plotContainer.pack_propagate(0)
        self.plotContainer.pack(side=TOP, anchor=N)
        self.mainFrame.pack_propagate(0)

        leftSide = Frame(self.mainFrame)
        button1 = TkinterCustomButton(master=leftSide, text="Segment",
                command=self.segment, corner_radius=60, height=25, width=120)
        button1.pack(side=TOP, pady=(10,0))
        button2 = TkinterCustomButton(master=leftSide, text="Browserview",
                command=self.viewBrowser, corner_radius=60, height=25, width=120)
        button2.pack(side=TOP, pady=(10,0))
        button3 = TkinterCustomButton(master=leftSide, text="Hide Edges" if self.showEdges else "Show Edges",
                command=self.changeEdgeView, corner_radius=60, height=25, width=120)
        button3.pack(side=TOP, pady=(10,0))
        leftSide.pack(side=LEFT, anchor=N, padx=(10,0))

        self.buttons.extend([button1, button2, button3])
        
        rightSide = Frame(self.mainFrame)
        self.list = ListView(rightSide, width=180, height=150).build()

        rightSide.pack(side=LEFT, anchor=N, padx=(20,10))
        self.mainFrame.pack(side=TOP, pady=(20,0))

    def deselectIfSelected(self):
        if self.selectedChart != -1:
            self.selectedChart = -1
            self.faceColors = self.refreshColors(self.selectedChart)
            self.show()


    def selectChart(self, chart):
        self.selectedChart = chart if self.selectedChart != chart else -1
        self.refreshChartDistortionInfo(self.selectedChart)
        self.faceColors = self.refreshColors(self.selectedChart)
        self.show()

    def refreshList(self):
        for child in self.list.winfo_children():
            child.destroy()

        cols = self.refreshColors()
        cols = self.faceColors
        for ch in self.chartList:
            if self.selectedChart != ch and self.selectedChart != -1: continue
            text = "Select" if self.selectedChart != ch else "Deselect"
            text += " Chart #" + str(ch)

            b = TkinterCustomButton(master=self.list, text=text,
             fg_color=cols[ch][:7], hover_color=cols[ch][:7], command=partial(self.selectChart, ch),
              corner_radius=60, height=25, width=170)
            b.pack(side=TOP, pady=(10,0))
            self.buttons.append(b)

    def getChartColor(self, chart:int):
        return self.chartToColor[chart]

    def refreshColors(self, selectedChart:int=-1):
        self.chartToColor = {}
        if selectedChart == -1:
            for index, val in enumerate(self.chartList):
                self.chartToColor[val] = distinctColors[index % len(distinctColors)]
            
        else:
            for index, val in enumerate(self.chartList):
                if val == selectedChart:
                    self.chartToColor[val] = distinctColors[index % len(distinctColors)]
                else:
                    self.chartToColor[val] = "#ffffff"

        colors = ["green"]*len(self.faces)
        for index, x in enumerate(self.charts): 
            color = self.chartToColor[x] + "ff"
            colors[index] = color

        return colors


    def plotFile(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.chartList = []
        self.charts = []
        self.faceColors = ["#1f77b4ff"] * len(faces)
        self.selectedChart = -1
        self.show()


    def segment(self):
        # abort if no file has been chosen
        if len(self.vertices) == 0: return
        self.charts, self.chartList = Segmenter(self.vertices, self.faces).calc()
        self.faceColors = self.refreshColors()
        self.selectedChart = -1
        self.show()


    def show(self):

        for b in self.buttons:
            b.delete()
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.build()
        
        root = self.plotContainer

        self.fig.clf()
        
        ax = self.fig.add_subplot(111, projection='3d')

        if len(self.faces) > 0:
            p3dc = ax.plot_trisurf(self.vertices[:, 0], self.vertices[:,1],
            triangles=self.faces, Z=self.vertices[:,2])
            p3dc.set_fc(self.faceColors)
            if self.showEdges:
                p3dc.set_edgecolor("black")


        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()

        self.canvas.mpl_connect("key_press_event", key_press_handler)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.refreshList()