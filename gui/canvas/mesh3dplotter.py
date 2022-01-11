from functools import total_ordering
from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib import cm
import igl

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


    def plotFile(self, vertices, faces):
        root = self.mainFrame
        for widget in root.winfo_children():
            widget.destroy()


        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')


        testC = ["#ff7f0eff"] * 6
        testC2 = ["#2ca02cff"] * 6

        testC.extend(testC2)

        p3dc = ax.plot_trisurf(vertices[:, 0], vertices[:,1], triangles=faces, Z=vertices[:,2])
        p3dc.set_fc(testC)


        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(self.canvas, root, pack_toolbar=False)
        toolbar.update()

        self.canvas.mpl_connect("key_press_event", key_press_handler)

        toolbar.pack(side=BOTTOM, fill=X)

        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
