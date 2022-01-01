import array
from functools import total_ordering
from typing import List
from openmesh import *
import numpy as np
from data_parser import SegmentationParser

max_string_length:int = 5
min_feature_length:int = 15
tao = 4

class Segmenter:

    def __init__(self, objPath:str):
        self.objPath = objPath
        self.parser = SegmentationParser()

    def getFeatures(self):
        featureCount = int(round(len(self.parser.SOD) * 0.05))
        features = {}
        for index, (key, value) in enumerate(self.parser.SOD.items()):
            if index >= featureCount: break
            features[key] = value
        
        return features.keys()

    def calc(self):
        self.parser.parse(self.objPath)
        relevantFeatures = self.getFeatures()
        self.marked_features = array.array('i',(False,)*self.parser.edgeLength())
        self.marked_feature_neighbors = array.array('i',(False,)*self.parser.edgeLength())
        for edge in relevantFeatures:
            self.expand_feature_curve(edge)

        print(relevantFeatures)

    def sharpness(self, s:List[int]):
        sum = 0
        for edge, _ in s:
            sum += self.parser.SOD[edge]
        return sum

    def getOtherVertex(self, edge:int, vertex:int):
        vertices = self.parser.edgeToVertices[edge]
        return vertices[1] if vertices[0]==vertex else vertices[0]

    def findEdgeString(self, edge:int, vertex:int, depth:int):
        if depth == max_string_length: return []

        maxString = []
        for neighbor in self.parser.mesh.ve(vertex):
            id = neighbor.idx()
            if id == edge: continue
            nextVertex = self.getOtherVertex(id, vertex)
            currentString = self.findEdgeString(id, nextVertex)
            maxString = currentString if self.sharpness(currentString) > self.sharpness(maxString) else maxString

        maxString.insert(0, (edge, vertex))
        return maxString



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
                s = self.findEdgeString(currentEdge, currentVertex, 0)

        #        append h' to detected_feature
                detected_feature.append(currentEdge)
        #        h' ← second item of S
                currentEdge, currentVertex = s[1]
    #        while(sharpness(S) > max_string_length × τ)
                if self.sharpness(s) > max_string_length * tao:
                    break
    #    end // for

    #    if (length(detected_feature) > min_feature_length) then
        if len(detected_feature) > min_feature_length:
    #        tag the elements of detected_feature as features
            for e in detected_feature:
                self.marked_features[e] = True
    #        tag the halfedges in the neighborhood of detected_feature as feature neighbors
            for e in detected_feature:
                faces = self.parser.edgeToFaces[e]
                for f in faces:
                    for eh in self.parser.mesh.fe(f):
                        id = eh.idx()
                        if id != e and id not in detected_feature:
                            self.marked_feature_neighbors[id] = True

    #    end // if

    def expand_charts():

    #    priority_queue<halfedge> Heap sorted by dist(facet(half edge))
    #    set<edge> chart_boundaries initialized with all the edges of the surface

    #    #Initialize Heap
    #    foreach facet F where dist(F ) is a local maximum
    #        create a new chart with seed F
    #        add the halfedges of F to Heap
    #    end // foreach

    #   #Charts-growing phase
    #   while(Heap is not empty)
    #        halfedge h ← e ∈ Heap such that dist(e) is maximum
    #        remove h from Heap
    #        facet F ← facet(h)
    #        facet Fopp ← the opposite facet of F relative to h

    #        if ( chart(Fopp) is undefined ) then
    #            add Fopp to chart(F )
    #            remove E from chart_boundaries
    #            remove non-extremal edges from chart_boundaries,
    #            #(i.e. edges that do not link two other chart boundary edges)
    #            add the halfedges of Fopp belonging to
    #            chart_boundaries to Heap

    #        elseif ( chart(Fopp) 6= chart(F ) and
    #            max_dist(chart(F )) - dist(F ) < ε and
    #            max_dist(chart(Fopp)) - dist(F ) < ε ) then
    #            merge chart(F ) and chart(Fopp)
    #        end // if
    #    end // while
        pass

print("init")
s = Segmenter("face.obj")
s.calc()
#print("ALL")
#s.printAll()
#print("SOD")
#print(s.parser.SOD)
#print("CUSTOM DATA")
#print(s.parser.edgeToFaces)