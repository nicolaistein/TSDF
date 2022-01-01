import igl
from openmesh import *
import numpy as np
from data_parser import SegmentationParser

class Segmenter:

    def __init__(self, objPath:str):
        self.objPath = objPath
        self.parser = SegmentationParser()

    def parseHalfedge(self):
        self.parser.parse(self.objPath)
        self.features = []

        edges = 0
        for eh in self.parser.mesh.edges():
            edges += 1

        print("edge count: " + str(edges))
        featureCount = int(round(len(self.parser.SOD) * 0.05))
        print("feature count: " + str(featureCount))
        features = {}
        for index, (key, value) in enumerate(self.parser.SOD.items()):
            if index >= featureCount: break
            features[key] = value

        print(features)


    def printAll(self):
        # iterate over all halfedges
        print("halfedges")
        for heh in self.parser.mesh.halfedges():
            print(heh.idx())
        # iterate over all edges
        print("edges")
        for eh in self.parser.mesh.edges():
            print(eh.idx())
        # iterate over all faces
        print("faces")
        for fh in self.parser.mesh.faces():
            print(fh.idx())

        vh1 = self.parser.vertexHandles[0]
        # iterate over all incoming halfedges
        print("incoming halfedges")
        for heh in self.parser.mesh.vih(vh1):
            print (heh.idx())
        # iterate over all outgoing halfedges
        print("outgoing halfedges")
        for heh in self.parser.mesh.voh(vh1):
            print (heh.idx())
        # iterate over all adjacent edges
        print("adjacent edges")
        for eh in self.parser.mesh.ve(vh1):
            print (eh.idx())
        # iterate over all adjacent faces
        print("adjacent faces")
        for fh in self.parser.mesh.vf(vh1):
            print(fh.idx())

    max_string_length:int = 5
    min_feature_length:int = 15

    def expand_feature_curve():
    #    vector<halfedge> detected_feature
        detected_feature = []
    #    for halfedge h ∈ { start, opposite(start) }
        
    #        halfedge h' ← h
    #        do
    #            use depth-first search to find the string S of halfedges
    #            starting with h' and such that:
    #            • two consecutive halfedges of S share a vertex
    #            • the length of S is 6 than max_string_length
    #            • sharpness(S) ←Ee∈S sharpness(e) is maximum
    #            • no halfedge of S goes backward (relative to h')
    #            • no halfedge of S is tagged as a feature neighbor
    #        h' ← second item of S
    #        append h to detected_f eature
    #        while(sharpness(S) > max_string_length × τ)
    #    end // for

    #    if (length(detected_f eature) > min_f eature_length) then
    #        tag the elements of detected_f eature as features
    #        tag the halfedges in the neighborhood of detected_f eature
    #            as feature neighbors
    #    end // if
        pass

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
s.parseHalfedge()
#print("ALL")
#s.printAll()
#print("SOD")
#print(s.parser.SOD)
#print("CUSTOM DATA")
#print(s.parser.edgeToFaces)