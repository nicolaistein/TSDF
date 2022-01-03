from typing import List
import array
import numpy as np
import bisect
from data_parser import SegmentationParser
from plotter import plotFaceColor
from priority_queue import PriorityQueue

prefix = "[Charts] "

def log(msg:str):
    print(prefix + msg)

class Charts:
    def __init__(self, parser:SegmentationParser):
        self.parser = parser

    def computeCharts(self, features:List[int]):
        self.features = features
        self.computeFeatureDistance()
        self.expand_charts()
    #    plotFaceColor(self.parser.vertices, self.parser.faces, self.featureDistances)
    #    print(self.featureDistances)


    def expandEdge(self, feature:int, edge:int, distance:int):

        newEdges = []
        handledFaces = 0
        for face in self.parser.edgeToFaces[edge]:
            if self.featureDistances[face] != -1: continue
            self.featureDistances[face] = distance
            handledFaces += 1
            newEdges.extend([e.idx() for e in self.parser.mesh.fe(self.parser.faceHandles[face]) if e.idx() != edge])
        
        self.featureBorders[feature].remove(edge)
        self.featureBorders[feature].extend(newEdges)
    #    log("expandEdge newEdges size: " + str(len(newEdges)) + ", handledFaces: " + str(handledFaces))

        return handledFaces

    def computeFeatureDistance(self):
        log("Computing feature distance")
        faceCount = len(self.parser.faces)
        self.featureDistances = {}
        self.featureBorders = [[]]*self.parser.edgeCount
        self.currentFeatureDistance = {}
        for f in self.features:
            self.featureBorders[f] = [f]
            self.currentFeatureDistance[f] = 0

        for index, _ in enumerate(self.parser.faces):
            self.featureDistances[index] = -1

        handledFaces = 0

        while handledFaces < faceCount and len(self.currentFeatureDistance) > 0:
            log("new round, handled faces: " + str(handledFaces) + ", remaining features: " + str(len(self.currentFeatureDistance)))
            toRemove = []
            for feature, distance in self.currentFeatureDistance.items():
                expanded = False
                for edge in self.featureBorders[feature]:
                    fc = self.expandEdge(feature, edge, distance)

                    handledFaces += fc
                    expanded = True if fc>0 else expanded
        #            log("expanded: " + str(expanded))

                self.currentFeatureDistance[feature] += 1
                if not expanded: toRemove.append(feature)
    #            else: print("feature was actually expanded")

        #    log("toRemove size: " + str(len(toRemove)))
            for f in toRemove:
                del self.currentFeatureDistance[f]
            

        log("while loop end")
        log("handled faces: " + str(handledFaces))
        log("faceCount: " + str(faceCount))
        log("current feature distance length: " + str(len(self.currentFeatureDistance)))


    def expand_charts(self):
        
    #    priority_queue<halfedge> Heap sorted by dist(facet(half edge))
        heap = PriorityQueue(self.featureDistances)

    #    set<edge> chart_boundaries initialized with all the edges of the surface
        chart_boundaries = [e.idx() for e in self.parser.mesh.edges()]

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
