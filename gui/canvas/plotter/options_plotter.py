from asyncio.windows_events import NULL
from typing import List

from pyparsing import col
from logger import log
from tkinter import *
from gui.canvas.plotting_options.plotting_option import PlottingOption
from gui.canvas.plotting_options.plotting_option_calculator import (
    PlottingOptionCalculator,
)


class OptionsPlotter:
    currentOption: PlottingOption = PlottingOption.NO_DIST

    def __init__(
        self,
        canvasManager,
        verticesToPlot,
        verticesBefore: List[List[float]],
        facesBefore: List[List[int]],
        verticesAfter: List[List[float]],
        facesAfter: List[List[int]],
        totalArea: float,
        color=None,
    ):
        self.cv = canvasManager
        self.canvas = canvasManager.canvas
        self.verticesToPlot = verticesToPlot
        self.color = color
        self.faces = facesAfter
        self.enabled = True
        self.distortionOnCanvas = []
        self.calculators = {}
        for e in PlottingOption:
            calc = e.getOptionCalculator(
                verticesBefore, facesBefore, verticesAfter, facesAfter, color, totalArea
            )
            if calc is not None:
                self.calculators[e.value] = calc

    def createLine(self, x1, x2):
        self.distortionOnCanvas.append(
            self.canvas.create_line(x1[0], x1[1], x2[0], x2[1])
        )

    def setOption(self, option: PlottingOption = PlottingOption.NO_DIST):
        self.currentOption = option
        self.refresh()

    def getDistortions(self, wholeObject: bool = False):
        if not wholeObject:
            return {typ: cal.totalDistortion for typ, cal in self.calculators.items()}
        return {
            typ: cal.totalDistortionWholeObject for typ, cal in self.calculators.items()
        }

    def refresh(self):
        self.clear()
        self.show()

    def show(self):
        if self.currentOption not in self.calculators:
            return
        calculator = self.calculators[self.currentOption]
        calculator.getDistortionValues()

        if not self.enabled:
            return
        colors = calculator.getColors()

        for index, face in enumerate(self.faces):

            x = list(self.verticesToPlot[face[0]])
            y = list(self.verticesToPlot[face[1]])
            z = list(self.verticesToPlot[face[2]])

            if index in colors:
                self.distortionOnCanvas.append(
                    self.canvas.create_polygon(x, y, z, fill=colors[index])
                )

    def clear(self):
        for point in self.distortionOnCanvas:
            self.canvas.delete(point)
        self.distortionOnCanvas.clear()

    def setEnabled(self, enabled: bool):
        self.enabled = enabled
        self.refresh()
