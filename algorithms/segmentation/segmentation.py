import array
from typing import List
from openmesh import *
import numpy as np
import time
from plotly import plot
from data_parser import SegmentationParser
from plotter import plot
import util

max_string_length:int = 5
min_feature_length:int = 15
tao = 23
featureCountPercentage = 0.05

class Segmenter:

    def __init__(self, objPath:str):
        self.objPath = objPath
        self.parser = SegmentationParser()

    def getFeatures(self):
        featureCount = int(round(len(self.parser.SOD) * featureCountPercentage))
        features = {}
        for index, (key, value) in enumerate(self.parser.SOD.items()):
            if index >= featureCount: break
            features[key] = value
        
        return features.keys()


    def calc(self):
        self.parser.parse(self.objPath)
        print("parsing finished")
        relevantFeatures = self.getFeatures()
        print("getting features finished")
        self.marked_features = array.array('i',(False,)*self.parser.edgeLength())
        self.marked_feature_neighbors = array.array('i',(False,)*self.parser.edgeLength())
        print("relevant feature size: " + str(len(relevantFeatures)))
        count = 0
        for edge in relevantFeatures:
            count += 1
            if count % 10 == 0: print("count: " + str(count))
            self.expand_feature_curve(edge)
        print("feature count: " + str(self.feature_count))
        colored = []
        fileContent = []
        print("calculation finished. Plotting...")
        for index, val in enumerate(self.marked_features):
            if val:
                vertices = self.parser.edgeToVertices[index]
                colored.append(vertices[0])
                colored.append(vertices[1])
                fileContent.append((vertices[0], vertices[1]))

        print("colored length: " + str(len(colored)))
        util.saveMarkedFeatures(fileContent)
        plot(self.parser.vertices, self.parser.faces, colored)
        

    def sharpness(self, s:List[int]):
        sum = 0
        for edge, _ in s:
            sum += self.parser.SOD[edge]
        return sum

    def getOtherVertex(self, edge:int, vertex:int):
        vertices = self.parser.edgeToVertices[edge]
        return vertices[1] if vertices[0]==vertex else vertices[0]

    def findEdgeString(self, edge:int, vertex:int, detected_feature:List[int], depth:int):
        if depth >= max_string_length: return []

        maxString = []
        for neighbor in self.parser.mesh.ve(self.parser.vertexHandles[vertex]):
            id = neighbor.idx()
            if id == edge: continue
            if self.marked_feature_neighbors[id]: continue
            if id in detected_feature: continue
            nextVertex = self.getOtherVertex(id, vertex)
            currentString = self.findEdgeString(id, nextVertex, detected_feature, depth+1)
            maxString = currentString if self.sharpness(currentString) > self.sharpness(maxString) else maxString

        maxString.insert(0, (edge, vertex))
        return maxString

    feature_count = 0


    def expand_feature_curve(self, edge:int):
    #    vector<halfedge> detected_feature
        detected_feature = []

        vertices = self.parser.edgeToVertices[edge]
        halfedges = [(edge, vertices[0]), (edge, vertices[1])]
    #    for halfedge h ∈ { start, opposite(start) }
        for e, v in halfedges:
    #        halfedge h' ← h
            currentEdge = e
            currentVertex = v
    #        do
            while True:
    #            use depth-first search to find the string S of halfedges
    #            starting with h' and such that:
    #            • two consecutive halfedges of S share a vertex
    #            • the length of S is 6 than max_string_length
    #            • sharpness(S) ←Ee∈S sharpness(e) is maximum
    #            • no halfedge of S goes backward (relative to h')
    #            • no halfedge of S is tagged as a feature neighbor
                s = self.findEdgeString(currentEdge, currentVertex, detected_feature, 0)

        #        print("s length: " + str(len(s)))
        #        print("sharpness s: " + str(self.sharpness(s)))

        #        append h' to detected_feature
                detected_feature.append(currentEdge)
        #        h' ← second item of S
                if len(s) < 2: break
                currentEdge, currentVertex = s[1]
    #        while(sharpness(S) > max_string_length × τ)
                if self.sharpness(s) <= max_string_length * tao: break
    #    end // for

    #    if (length(detected_feature) > min_feature_length) then
        if len(detected_feature) > min_feature_length:
            self.feature_count += 1
    #        print("accepted feature length: " + str(len(detected_feature)))
    #        tag the elements of detected_feature as features
            for e in detected_feature:
                self.marked_features[e] = True
    #        tag the halfedges in the neighborhood of detected_feature as feature neighbors
            for e in detected_feature:
                faces = self.parser.edgeToFaces[e]
                for f in faces:
                    for eh in self.parser.mesh.fe(self.parser.faceHandles[f]):
                        id = eh.idx()
                        if id != e and id not in detected_feature:
                            self.marked_feature_neighbors[id] = True

    #    end // if


    

print("init")
s = Segmenter("face.obj")
computeStart = time.time()
s.calc()
computeEnd = time.time()
print("time: " + str(computeEnd-computeStart))
print("Tao: " + str(tao))
print("Feature count: " + str(featureCountPercentage))
#print("ALL")
#s.printAll()
#print("SOD")
#print(s.parser.SOD)
#print("CUSTOM DATA")
#print(s.parser.edgeToFaces)