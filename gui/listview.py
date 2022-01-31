from tkinter import *
from tkinter import ttk
from logger import log

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
        self.innerContent.update()
        self.canvas.update()
        canvasHeight = self.canvas.winfo_reqheight()
        innerHeight = self.innerContent.winfo_reqheight()

        if canvasHeight > innerHeight: return
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def reset_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def build(self):
        self.canvas = Canvas(self.container, height=self.height,
             width=self.width, bg=self.bg, bd=0, highlightthickness=0)
        self.innerContent = Frame(self.canvas, padx=self.padx, bg=self.bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(self.container, orient=VERTICAL, command=self.canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=my_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.canvas.create_window((0,0), window=self.innerContent, anchor=NW)
        self.innerContent.bind('<Enter>', self._bound_to_mousewheel)
        self.innerContent.bind('<Leave>', self._unbound_to_mousewheel)
        self.innerContent.bind("<Configure>", self.reset_scrollregion)

        return self.innerContent