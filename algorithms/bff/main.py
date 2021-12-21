import subprocess
import platform


class BFF:
    def __init__(self, coneCount, objPath):
        self.coneCount = coneCount
        self.objPath = objPath

    def execute(self):
        # Select binary depending on the os
        print("Platform: " + platform.system())
        commandPath = "./algorithms/bff/unix/bff-command-line"
        if(platform.system() == "Windows"):
            commandPath = "./algorithms/bff/windows/bff-command-line.exe"

        # Execute BFF
        execute_bff = subprocess.run(
            [commandPath, self.objPath, "./algorithms/bff/result.obj", "--nCones=%s" % (self.coneCount)])

        resultFile = open("./algorithms/bff/result.obj", "r")
        content = resultFile.read()

        # Extract texture vertices
        finalResult = []
        lines = content.split("\n")
        for line in lines:
            if(line.startswith("vt")):
                split = line.split(" ")
                finalResult.append([float(split[1]), float(split[2])])

        return finalResult
