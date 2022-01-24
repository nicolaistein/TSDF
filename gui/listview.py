from tkinter import *
from tkinter import ttk


def getListview(container:Frame, width:int, height:int, padx=10, bg=None):
        canvas = Canvas(container, height=height, width=width, bg=bg, bd=0, highlightthickness=0)
        innerContent = Frame(canvas, padx=padx, bg=bg)

        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        # Add that New frame To a Window In The Canvas
        canvas.create_window((0,0), window=innerContent, anchor=NW)
        return innerContent