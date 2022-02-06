# pyinstaller main.py --onedir --add-data algorithms/bff/win -n "GCodePatternManager"

import PyInstaller.__main__
import shutil

oneFile:bool = False
name:str = "GCodePatternManager"

def copy(path:str):
    dirName = "" if oneFile else name + "/"
    shutil.copytree(path, 'dist/' + dirName + path)


PyInstaller.__main__.run([
    'main.py',
    '-n=' + name,
    '--icon=image.ico',
    '--onefile' if oneFile else "--onedir",
], )

copy("algorithms/bff/windows")
copy("algorithms/bff/unix")

#shutil.copytree('algorithms/bff/windows', 'dist/algorithms/bff/window')
#shutil.copytree('algorithms/bff/windows', 'dist/algorithms/bff/window')