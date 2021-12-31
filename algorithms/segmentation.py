from os import read
from typing import List
import igl
from openmesh import *
import numpy as np

class Segmenter:

    def __init__(self, objPath:str):
        self.objPath = objPath

    def parseHalfedge(self):
        self.vertices, self.faces = igl.read_triangle_mesh(self.objPath)
        self.mesh = TriMesh()
        self.vertexHandles = []
        self.faceHandles = []
        for v in self.vertices:
            self.vertexHandles.append(self.mesh.add_vertex([v[0], v[1], 0 if len(v) < 3 else v[2]]))

        for f in self.faces:
            self.faceHandles.append(self.mesh.add_face(self.vertexHandles[f[0]], self.vertexHandles[f[1]], self.vertexHandles[f[2]]))

        print("Reading finisehd")


    def surface_normal(self, faceID:int):
        face = self.faces[faceID]
        p1 = self.vertices[face[0]]
        p2 = self.vertices[face[1]]
        p3 = self.vertices[face[2]]
        a = p2-p1
        b = p3-p1
        v = np.cross(a,b)
        normalized_v = v / np.sqrt(np.sum(v**2))

        return normalized_v

    

    def compute_SOD_all(self):
        self.SOD = {}
        for face in self.mesh.faces():
            f1ID = face.idx()
            self.SOD[f1ID] = {}
            n1 = self.surface_normal(f1ID)
            for face2 in self.mesh.ff(face):
                f2ID = face2.idx()
                n2 = self.surface_normal(f2ID)
                result = np.degrees(np.arccos(np.dot(n1, n2)))
                self.SOD[f1ID][f2ID] = result

        print("SOD finished")
        print(self.SOD) 

    def printAll(self):
        # iterate over all halfedges
        print("halfedges")
        for heh in self.mesh.halfedges():
            print(heh.idx())
        # iterate over all edges
        print("edges")
        for eh in self.mesh.edges():
            print(eh.idx())
        # iterate over all faces
        print("faces")
        for fh in self.mesh.faces():
            print(fh.idx())

        vh1 = self.vertexHandles[0]
        # iterate over all incoming halfedges
        print("incoming halfedges")
        for heh in self.mesh.vih(vh1):
            print (heh.idx())
        # iterate over all outgoing halfedges
        print("outgoing halfedges")
        for heh in self.mesh.voh(vh1):
            print (heh.idx())
        # iterate over all adjacent edges
        print("adjacent edges")
        for eh in self.mesh.ve(vh1):
            print (eh.idx())
        # iterate over all adjacent faces
        print("adjacent faces")
        for fh in self.mesh.vf(vh1):
            print(fh.idx())

    max_string_length:int = 5
    min_feature_length:int = 15

    def expand_feature_curve():
    #    vector<halfedge> detected_f eature
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
s.compute_SOD_all()