from tkinter import *
from tkinter.filedialog import askdirectory
from gui.button import TkinterCustomButton
from gui.filemenu import Menu as MenuWidget

root = Tk()
root.title("SuPa")
# root.iconbitmap("Path/to/test.ico")
root.geometry("1120x840")
root.configure(bg="#cccccc")

canvasSize = 800

canvasFrame = Frame(root, height=canvasSize, width=canvasSize)
canvas = Canvas(canvasFrame, height=canvasSize, width=canvasSize)
leftContainer = Frame(root, bg="#cccccc", pady=20)

menu = MenuWidget(leftContainer, canvas,)

menu.build("top")


def export():
    filename = askdirectory()
    file = open(filename + "/result.supa", "w")
    for x, y in menu.points:
        file.write(str(x) + " " + str(y) + "\n")
    file.close()


TkinterCustomButton(master=leftContainer, text="Export Result", command=export,
                    corner_radius=60, height=25, width=140).pack(side="top", pady=0)

leftContainer.pack(side="left", padx=0, anchor=N)
canvas.pack(side="top")
canvasFrame.pack(side="left")

root.mainloop()
