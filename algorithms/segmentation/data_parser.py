import igl
from openmesh import *
import numpy as np
import array
import math

prefix = "[Halfedge Parser] "

def log(msg:str):
    print(prefix + msg)

class SegmentationParser:    
    """
    faces: List of faces
    vertices: List of vertices
    SOD: mapping face1:face2 -> SOD
    edgeToFaces: mapping edge -> List of faces 
    """

    def parse(self, objPath:str, sod:bool=True):
        self.vertices, self.faces = igl.read_triangle_mesh(objPath)
        log("vertex length: " + str(len(self.vertices)))
        log("faces length: " + str(len(self.faces)))
        self.createMesh()
        self.edgeCount = len(self.mesh.edges())
        log("edge count: " + str(self.edgeCount))
        self.readCustomData()
        if sod: self.compute_SOD_all()
   

        log("Reading finisehd")

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
        self.edgeToFaces = {}
        for face in self.mesh.faces():
            fid = face.idx()
            for edge in self.mesh.fe(face):
                id = edge.idx()
                if id not in self.edgeToFaces: self.edgeToFaces[id] = []
                self.edgeToFaces[id].append(fid)

        self.edgeToVertices = {}
        for vertex in self.mesh.vertices():
            vid = vertex.idx()
            for edge in self.mesh.ve(vertex):
                id = edge.idx()
                if id not in self.edgeToVertices: self.edgeToVertices[id] = []
                self.edgeToVertices[id].append(vid)


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
        log("computing SOD...")
        self.SOD = {}
        for index, val in self.edgeToFaces.items():
            if len(val) < 2:
                #Edge is at the border loop
                result = 360
            else:
                n1 = self.surface_normal(val[0])
                n2 = self.surface_normal(val[1])
                result = np.degrees(np.arccos(np.dot(n1, n2)))
            self.SOD[index] = result

        log("sorting...")
        self.SOD = {k: v for k, v in sorted(self.SOD.items(), key=lambda item: item[1], reverse=True)}
        log("computing SOD finished")


    
