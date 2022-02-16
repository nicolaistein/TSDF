from tkinter import *
from typing import Mapping
from logger import log
from gui.button import TkinterCustomButton
from gui.menu_heading.info_window import InfoWindow


class MenuHeading:

    def __init__(self, title:str, mapping:Mapping=None):
        self.title = title
        self.mapping = mapping

    def onInfo(self):
        InfoWindow(self.master, self.title, self.mapping).openWindow()


    def build(self, master: Frame):
        self.master = master
        content = Frame(master)
        title = Label(content, text=self.title)
        title.configure(font=("Helvetica", 12, "bold"))
        title.pack(fill='both', side=LEFT)

        if self.mapping is not None:
            TkinterCustomButton(master=content, text="Help", command=self.onInfo, fg_color="#c2c2c2",
                            hover_color="#c75454",
                            corner_radius=10, height=20, width=50).pack(side=TOP, padx=(6, 0), pady=(2, 0))

        content.pack(side=TOP, pady=(0, 15))

