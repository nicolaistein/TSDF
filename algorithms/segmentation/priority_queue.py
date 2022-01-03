from typing import List, Mapping
import bisect

prefix = "[Priority Queue] "

def log(msg:str):
    print(prefix + msg)

class PriorityQueue:
    def __init__(self, featureDistances:Mapping):
        self.featureDistances = featureDistances
        self.keys = []
        self.values = []

    def pop(self):
        key = self.keys.pop(0)
        value = self.values.pop(0)
        return key, value

    def insert(self, key:int):
        val = self.featureDistances[key]
    #    log("insert key: " + str(key) + ", feature distance: " + str(val))
        idx = bisect.bisect_left(self.values, val)
        self.values.insert(idx, val)
    #    log("insert idx: " + str(idx))
        self.keys.insert(idx, key)

    #    log("insert keySize: " + str(len(self.keys)) + ", valueSize: " + str(len(self.values)))
    #    print("keys  : " + str(self.keys))
    #    print("values: " + str(self.values))

    def print(self):
        for index, key in enumerate(self.keys):
            log(str(key) + ": " + str(self.values[index]))
