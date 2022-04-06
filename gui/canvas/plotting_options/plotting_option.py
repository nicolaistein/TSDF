from enum import Enum
from typing import List
from logger import log
from tkinter import *
from gui.canvas.plotting_options.calculators.lscm_calculator import LscmCalculator
from gui.canvas.plotting_options.calculators.default_calculator import DefaultCalculator
from gui.canvas.plotting_options.calculators.face_colors_calculator import (
    FaceColorsCalculator,
)
from gui.canvas.plotting_options.calculators.arap_calculator import ArapCalculator
from gui.canvas.plotting_options.calculators.maximal_isometric_calculator import (
    MaximalIsometricCalculator,
)
from gui.canvas.plotting_options.calculators.efficient_isometric_calculator import (
    EfficientIsometricCalculator,
)


class PlottingOption(Enum):
    NO_DIST = 0
    COLORS = 1
    LSCM = 2
    ARAP = 3
    MAX_ISOMETRIC = 4
    EFFICIENT_ISOMETRIC = 5

    def toString(self):
        switcher = {
            0: "Default",
            1: "Chart Colors",
            2: "Angular Dist.",
            3: "Isometric Dist.",
            4: "Max. isom. Dist.",
            5: "Fast isom. Dist.",
        }
        return switcher[self.value]

    def getOptionCalculator(
        self,
        verticesBefore: List[List[float]],
        facesBefore: List[List[int]],
        verticesAfter: List[List[float]],
        facesAfter: List[List[int]],
        color,
        totalArea: float,
    ):

        switcher = {
            0: DefaultCalculator,
            1: FaceColorsCalculator,
            2: LscmCalculator,
            3: ArapCalculator,
            4: MaximalIsometricCalculator,
            5: EfficientIsometricCalculator,
        }

        calculator = switcher[self.value]

        return calculator(
            verticesBefore,
            facesBefore,
            verticesAfter,
            facesAfter,
            self,
            color,
            totalArea,
        )

    def getMinMax(self):
        """Returns minimal, optimal and maximal distortion. If not available None is returned

        Returns:
            Tuple(int): (minDist, optimalDist, maxDist)
        """
        switcher = {
            0: (None, None, None),
            1: (None, None, None),
            2: (None, 0, 0.4),
            3: (None, 0, 0.8),
            4: (None, 1, 1.8),
            5: (0, 4, 10),
        }
        return switcher[self.value]

    def getColor(self):
        switcher = {
            0: None,
            1: None,
            2: (255, 0, 0),
            3: (0, 0, 255),
            4: (255, 105, 36),
            5: [(65, 30, 148), (255, 0, 0)],
        }
        return switcher[self.value]

    def getColormap(
        self,
        canvas: Canvas,
        width: int,
        height: int,
        reverse: bool = False,
        optionColor=None,
    ):
        if optionColor is None:
            optionColor = self.getColor()

        if type(optionColor) is not tuple:
            return

        r, g, b = optionColor

        stepSizeR = (255 - r) / width
        stepSizeG = (255 - g) / width
        stepSizeB = (255 - b) / width

        for x in range(width):
            for y in range(height):

                colorFacR = int(round(stepSizeR * x, 0))
                colorFacG = int(round(stepSizeG * x, 0))
                colorFacB = int(round(stepSizeB * x, 0))

                color = "#%02x%02x%02x" % (
                    255 - colorFacR,
                    255 - colorFacG,
                    255 - colorFacB,
                )

                if reverse:
                    x = width - x
                canvas.create_oval(x, y, x, y, fill=color, width=0)
