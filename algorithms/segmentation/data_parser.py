import igl
from openmesh import *
import numpy as np

class SegmentationParser:    
    """
    faces: List of faces
    vertices: List of vertices
    SOD: mapping face1:face2 -> SOD
    edgeToFaces: mapping edge -> List of faces 
    """

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
            for edge in self.mesh.fe(face):
                id = edge.idx()
                if id not in self.edgeToFaces: self.edgeToFaces[id] = []
                self.edgeToFaces[id].append(face.idx())

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
        self.createMesh()
        self.readCustomData()
        self.compute_SOD_all()
   

        print("Reading finisehd")
