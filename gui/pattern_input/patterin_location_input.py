from functools import partial
from tkinter import *
from typing import List, Mapping
from gui.button import TkinterCustomButton
from gui.pattern_input.custom_text import CustomText
from gui.pattern_input.pattern_input_line import PatternInputLine


class PatternLocationInput(PatternInputLine):

    def pick(self):
        print("PatternLocationInput pick")
        self.window.pickLocation()

    def build(self, master: Frame, pady: float, textWidth=4):
        super().build(master, pady, textWidth)

        self.button = TkinterCustomButton(master=self.mainContainer, text="Pick", command=self.pick,
                                          corner_radius=60, height=25, width=80)
        self.button.pack(side=LEFT, padx=(10, 0))


