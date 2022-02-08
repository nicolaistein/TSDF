from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from gui.button import TkinterCustomButton
from algorithms.algorithms import *
from gui.canvas.canvas_manager import CanvasManager
from logger import log


class ExportMenu:
    mainFrame:Frame = None
    button:TkinterCustomButton = None

    def __init__(self, master: Frame, canvasManager: CanvasManager):
        self.master = master
        self.canvasManager = canvasManager
        self.plotter = canvasManager.measurePlotter

    def buttonClick(self):
        if len(self.canvasManager.objectPlotters) == 0: return
        folder = askdirectory()
        if not os.path.isdir(folder): return
        file = open(folder + "/shapes.obj", "w")

        shifts = [0]
        for pl in self.canvasManager.objectPlotters:
            shifts.append(shifts[-1]+len(pl.verticesForExport))
            for v in pl.verticesForExport:
                x, y = self.canvasManager.reverseP(v[0], v[1])
                file.write("v " + str(v[0]) + " " + str(v[1]) + " 0\n")

        for index, pl in enumerate(self.canvasManager.objectPlotters):
            shift = shifts[index]
            for f in pl.faces:
                file.write("f")
                for v in f:
                    file.write(" " + str(v+shift+1))
                file.write("\n")
        file.close()

        length = len(self.canvasManager.objectPlotters)
        text = "shape" if length == 1 else "shapes"
        messagebox.showinfo("Export", "Successfully exported "
         + str(length) + " " + text + " to " + file.name)

    def refreshView(self):
        self.button.delete()
        for child in self.mainFrame.winfo_children():
            child.destroy()
        self.mainFrame.destroy()
        self.build()

    def build(self):
        self.mainFrame = Frame(self.master, width=260, height=120, padx=20, pady=20)
        title = Label(self.mainFrame, text="Export Flat Shapes")
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=TOP, pady=(0, 15))

        self.mainFrame.pack_propagate(0)

        self.button = TkinterCustomButton(master=self.mainFrame, text="Export", command=self.buttonClick,
                            corner_radius=60, height=25, width=100)
        self.button.pack(side=TOP)

        self.mainFrame.pack(side=TOP, pady=(2, 0))