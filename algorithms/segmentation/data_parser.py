import igl
from openmesh import *
import numpy as np
import array

class SegmentationParser:    
    """
    faces: List of faces
    vertices: List of vertices
    SOD: mapping face1:face2 -> SOD
    edgeToFaces: mapping edge -> List of faces 
    """

    def calculateEdgeCount(self):
        self.edgeCount = 0
        for edge in self.mesh.edges:
            self.edgeCount += 1

    def createMesh(self):
        self.mesh = TriMesh()
        self.vertexHandles = []
        self.faceHandles = []
        for v in self.vertices:
            self.vertexHandles.append(self.mesh.add_vertex([v[0], v[1], 0 if len(v) < 3 else v[2]]))

        for f in self.faces:
            self.faceHandles.append(self.mesh.add_face(self.vertexHandles[f[0]],
                self.vertexHandles[f[1]], self.vertexHandles[f[2]]))

    def readCustomData(self):
        self.edgeToFaces = array.array('i',([],)*self.edgeCount)
        for face in self.mesh.faces():
            fid = face.idx()
            for edge in self.mesh.fe(face):
                self.edgeToFaces[edge.idx()].append(fid)

        self.edgeToVertices = array.array('i',([],)*self.edgeCount)
        for vertex in self.mesh.vertices():
            vid = vertex.idx()
            for edge in self.mesh.ve(vertex):
                self.edgeToVertices[edge.idx()].append(vid)


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
        print("computing SOD...")
        self.SOD = {}
        for key, val in self.edgeToFaces.items():
            if len(val) < 2:
                #Edge is at the border loop
                result = 360
            else:
                n1 = self.surface_normal(val[0])
                n2 = self.surface_normal(val[1])
            result = np.degrees(np.arccos(np.dot(n1, n2)))
            self.SOD[key] = result

        print("sorting...")
        self.SOD = {k: v for k, v in sorted(self.SOD.items(), key=lambda item: item[1], reverse=True)}
        print("computing SOD finished")


    def parse(self, objPath:str):
        self.vertices, self.faces = igl.read_triangle_mesh(objPath)
        print("vertex length: " + str(len(self.vertices)))
        print("faces length: " + str(len(self.faces)))
        self.createMesh()
        self.calculateEdgeCount()
        self.readCustomData()
        self.compute_SOD_all()
   

        print("Reading finisehd")


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