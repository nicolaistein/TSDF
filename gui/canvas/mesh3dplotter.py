from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import igl



class Mesh3DPlotter:

    def __init__(self, master: Frame):
        self.mainFrame = Frame(master, width=400, height=400)

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


    def draw2(self):
        root = self.mainFrame
        v, f = igl.read_triangle_mesh("algorithms/segmentation/Part_1.obj")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(v[:, 0], v[:,1], triangles=f, Z=v[:,2]) 


        self.canvas = FigureCanvasTkAgg(fig, master=root)
        self.canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(self.canvas, root, pack_toolbar=False)
        toolbar.update()

        self.canvas.mpl_connect("key_press_event", key_press_handler)

        toolbar.pack(side=BOTTOM, fill=X)

        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
