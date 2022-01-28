from tkinter import *
from tkinter import ttk

class ListView:

    def __init__(self, container:Frame, width:int, height:int, padx=10, bg=None):
        self.container = container
        self.width = width
        self.height = height
        self.padx = padx
        self.bg = bg

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def build(self):
        self.canvas = Canvas(self.container, height=self.height,
             width=self.width, bg=self.bg, bd=0, highlightthickness=0)
        innerContent = Frame(self.canvas, padx=self.padx, bg=self.bg)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(self.container, orient=VERTICAL, command=self.canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        self.canvas.configure(yscrollcommand=my_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        # Add that New frame To a Window In The Canvas
        self.canvas.create_window((0,0), window=innerContent, anchor=NW)
        innerContent.bind('<Enter>', self._bound_to_mousewheel)
        innerContent.bind('<Leave>', self._unbound_to_mousewheel)

        return innerContent