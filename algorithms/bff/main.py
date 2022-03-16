import subprocess
import platform
from logger import log


class BFF:
    def __init__(self, coneCount, objPath):
        self.coneCount = coneCount
        self.objPath = objPath

    def getTextureVertex(self, val: str):
        return int(val.split("/")[1])

    def execute(self):
        # Select binary depending on the os
        log("Platform: " + platform.system())
        commandPath = "./algorithms/bff/unix/bff-command-line"
        if platform.system() == "Windows":
            commandPath = "./algorithms/bff/windows/bff-command-line.exe"

        # Execute BFF
        subprocess.run(
            [
                commandPath,
                self.objPath,
                "./algorithms/bff/result.obj",
                "--nCones=%s" % (self.coneCount),
            ]
        )

        resultFile = open("./algorithms/bff/result.obj", "r")
        content = resultFile.read()

        # Extract texture vertices
        vertices = []
        faces = []
        lines = content.split("\n")
        for line in lines:
            if line.startswith("vt"):
                split = line.split(" ")
                vertices.append([float(split[1]), float(split[2])])

            elif line.startswith("f"):
                split = line.split(" ")
                x1 = self.getTextureVertex(split[1])
                x2 = self.getTextureVertex(split[2])
                x3 = self.getTextureVertex(split[3])
                faces.append([x2, x3, x1])

        return vertices, faces
