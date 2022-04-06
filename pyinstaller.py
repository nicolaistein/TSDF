import PyInstaller.__main__
import shutil

name: str = "TSDF"


def copyFolder(path: str):
    shutil.copytree(path, "dist/" + path)


def copyFile(path: str):
    shutil.copyfile(path, "dist/" + path)


PyInstaller.__main__.run(
    [
        "main.py",
        "-n=" + name,
        "--icon=image.ico",
        "--onefile",
    ],
)

copyFolder("algorithms/bff/windows")
copyFolder("algorithms/bff/unix")
copyFolder("patterns")
copyFile("image.ico")
