import PyInstaller.__main__
import shutil

oneFile: bool = True
name: str = "TSDF"


def copy(path: str):
    dirName = "" if oneFile else name + "/"
    shutil.copytree(path, "dist/" + dirName + path)


PyInstaller.__main__.run(
    [
        "main.py",
        "-n=" + name,
        "--icon=image.ico",
        "--onefile" if oneFile else "--onedir",
    ],
)

copy("algorithms/bff/windows")
copy("algorithms/bff/unix")
copy("patterns")
