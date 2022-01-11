from functools import total_ordering
from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib import cm
from algorithms.segmentation.segmentation import Segmenter
import igl

distinctColors = ["#808080", "#dcdcdc", "#556b2f", "#8b4513", "#228b22", "#483d8b", "#b8860b",
    "#008b8b", "#000080", "#9acd32", "#8fbc8f", "#800080", "#b03060", "#ff0000", "#ffff00",
    "#deb887", "#00ff00", "#8a2be2", "#00ff7f", "#dc143c", "#00ffff", "#00bfff", "#0000ff", "#ff7f50",
    "#ff00ff", "#1e90ff", "#dda0dd", "#90ee90", "#ff1493", "#7b68ee"]


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)


class Mesh3DPlotter:

    def __init__(self, master: Frame):
        self.mainFrame = Frame(master, width=360, height=360)

    def update_frequency(self, new_val):
        # retrieve frequency
        f = float(new_val)

        # update data
        y = 2 * np.sin(2 * np.pi * f * self.t)
        self.line.set_data(self.t, y)

        # required to update canvas and attached toolbar!
        self.canvas.draw()


    def build(self):
        self.mainFrame.pack_propagate(0)
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


    def plotFile(self, vertices, faces, objFile):
        root = self.mainFrame
        for widget in root.winfo_children():
            widget.destroy()


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')


        testC = ["#ff7f0eff"] * 6
        testC2 = ["#2ca02cff"] * 6

        testC.extend(testC2)


        charts, chartList = Segmenter(objFile).calc()
        colors = self.getColors(faces, charts, chartList)

        p3dc = ax.plot_trisurf(vertices[:, 0], vertices[:,1], triangles=faces, Z=vertices[:,2])
        p3dc.set_fc(colors)
    #    p3dc.set_edgecolor("black")


        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(self.canvas, root, pack_toolbar=False)
        toolbar.update()

        self.canvas.mpl_connect("key_press_event", key_press_handler)

        toolbar.pack(side=BOTTOM, fill=X)

        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
