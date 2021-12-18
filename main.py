from tkinter import *
from tkinter.filedialog import askdirectory
from gui.file_menu import FileMenu
from gui.scale_menu import ScaleMenu
from gui.gcode_menu import GCodeMenu
from gui.pattern_list.placed_patterns_menu import PlacedPatternsMenu

mainColor = "#cccccc"
root = Tk()
root.title("GCode Pattern Manager")
root.resizable(False, False)
# root.iconbitmap("Path/to/test.ico")
root.geometry("1920x1080")
root.configure(bg=mainColor, padx=20, pady=20)

canvasSize = 900

canvasFrame = Frame(root, height=canvasSize, width=canvasSize)
canvas = Canvas(canvasFrame, height=canvasSize, width=canvasSize)
leftContainer = Frame(root, bg=mainColor)

menu = FileMenu(leftContainer, canvas)
menu.build("top")
ScaleMenu(leftContainer).build("top")


def export():
    filename = askdirectory()
    file = open(filename + "/result.supa", "w")
    for x, y in menu.points:
        file.write(str(x) + " " + str(y) + "\n")
    file.close()


leftContainer.pack(side="left", padx=(0, 20), anchor=N)
canvasFrame.pack(side="left", anchor=N)
GCodeMenu(root, mainColor).build("left")
PlacedPatternsMenu(root, mainColor).build("left")
canvas.pack(side="left")

root.mainloop()
