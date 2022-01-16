from functools import total_ordering
from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import numpy as np
from gui.button import TkinterCustomButton
from algorithms.segmentation.plotter import plotFaceColors, distinctColors
from algorithms.segmentation.segmentation import Segmenter

class Mesh3DPlotter:

    def __init__(self, master: Frame):
        self.mainFrame = Frame(master, width=360, height=480)
        self.buttons = []
        self.faces = []
        self.vertices = []
        self.faceColors = []
        self.showEdges = False

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

        self.buttons = [button1, button2, button3]
        
        rightSide = Frame(self.mainFrame)

        rightSide.pack(side=LEFT, anchor=N, padx=(0,10))

        self.mainFrame.pack(side=TOP, pady=(20,0))


    def getColors(self, faces, charts, chartList):
        chartToColor = {}
        for index, val in enumerate(chartList):
            chartToColor[val] = distinctColors[index % len(distinctColors)]

        colors = ["green"]*len(faces)
        for index, x in enumerate(charts): 
            color = chartToColor[x] + "ff"
            colors[index] = color

        return colors


    def plotFile(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.faceColors = ["#1f77b4"] * len(faces)
        self.show()


    def segment(self):
        charts, chartList = Segmenter(self.vertices, self.faces).calc()
        self.faceColors = self.getColors(self.faces, charts, chartList)
        self.show()


    def show(self):

        for b in self.buttons:
            b.delete()
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.build()
        
        root = self.plotContainer

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        if len(self.faces) > 0:
            p3dc = ax.plot_trisurf(self.vertices[:, 0], self.vertices[:,1],
            triangles=self.faces, Z=self.vertices[:,2])
            p3dc.set_fc(self.faceColors)
            if self.showEdges:
                p3dc.set_edgecolor("black")


        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.draw()

        self.canvas.mpl_connect("key_press_event", key_press_handler)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)