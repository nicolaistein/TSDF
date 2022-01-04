from typing import List, Mapping
import bisect

prefix = "[Priority Queue] "

def log(msg:str):
    print(prefix + msg)

class PriorityQueue:
    def __init__(self, featureDistances:Mapping):
        self.featureDistances = featureDistances
        self.data = []
        self.values = []

    def pop(self):
        index = len(self.data) - 1
        face, edge = self.data.pop(index)
        value = self.values.pop(index)
        return face, edge

    def insert(self, face:int, edge:int):
        val = self.featureDistances[face]
    #    log("insert key: " + str(key) + ", feature distance: " + str(val))
        idx = bisect.bisect_left(self.values, val)
        self.values.insert(idx, val)
    #    log("insert idx: " + str(idx))
        self.data.insert(idx, (face, edge))

    #    log("insert keySize: " + str(len(self.keys)) + ", valueSize: " + str(len(self.values)))
    #    print("keys  : " + str(self.keys))
    #    print("values: " + str(self.values))

    def print(self):
        for index, face, edge in enumerate(self.data.items()):
            log(str(face) + " " + str(edge) + ": " + str(self.values[index]))

    def size(self):
        return len(self.data)
