from typing import List
from openmesh import *
import numpy as np
from logger import log


class SegmentationParser:
    """
    Parses the mesh into the halfedge data structure
    """

    def parse(
        self, vertices: List[List[float]], faces: List[List[int]], sod: bool = True
    ):
        """main method that manages the parsing process

        Args:
            vertices (List[List[float]]): vertices
            faces (List[List[int]]): faces
            sod (bool, optional): Indicates whether SOD values need to be calculated. Defaults to True.
        """
        self.vertices = vertices
        self.faces = faces
        log("vertex length: " + str(len(self.vertices)))
        log("faces length: " + str(len(self.faces)))
        self.createMesh()
        self.edgeCount = len(self.mesh.edges())
        log("edge count: " + str(self.edgeCount))
        self.createCustomMappings()
        if sod:
            self.compute_SOD_all()

        log("Reading finisehd")

    def createMesh(self):
        """Creates the halfedge data structure"""
        self.mesh = TriMesh()
        self.vertexHandles = []
        self.faceHandles = []
        for v in self.vertices:
            self.vertexHandles.append(
                self.mesh.add_vertex([v[0], v[1], 0 if len(v) < 3 else v[2]])
            )

        for f in self.faces:
            self.faceHandles.append(
                self.mesh.add_face(
                    self.vertexHandles[f[0]],
                    self.vertexHandles[f[1]],
                    self.vertexHandles[f[2]],
                )
            )

    def createCustomMappings(self):
        """Creates mappings to provide additional connectivity"""
        # Mapping 1 (edge index to adjacent faces)
        self.edgeToFaces = {}
        for face in self.mesh.faces():
            fid = face.idx()
            for edge in self.mesh.fe(face):
                id = edge.idx()
                if id not in self.edgeToFaces:
                    self.edgeToFaces[id] = []
                self.edgeToFaces[id].append(fid)

        # Mapping 2 (edge index to adjacent vertices)
        self.edgeToVertices = {}
        for vertex in self.mesh.vertices():
            vid = vertex.idx()
            for edge in self.mesh.ve(vertex):
                id = edge.idx()
                if id not in self.edgeToVertices:
                    self.edgeToVertices[id] = []
                self.edgeToVertices[id].append(vid)

    def surface_normal(self, faceID: int):
        """Computes the normal of a face

        Args:
            faceID (int): the face

        Returns:
            List[float]: normal vector
        """
        face = self.faces[faceID]
        p1 = self.vertices[face[0]]
        p2 = self.vertices[face[1]]
        p3 = self.vertices[face[2]]
        a = p2 - p1
        b = p3 - p1
        v = np.cross(a, b)
        normalized_v = v / np.sqrt(np.sum(v**2))

        return normalized_v

    def compute_SOD_all(self):
        """Computes the second order difference of all edges"""
        log("computing SOD...")
        self.SOD = {}
        for index, val in self.edgeToFaces.items():
            if len(val) < 2:
                # Edge is at the border loop
                result = 360
            else:
                n1 = self.surface_normal(val[0])
                n2 = self.surface_normal(val[1])
                result = np.degrees(np.arccos(np.dot(n1, n2)))
            self.SOD[index] = result

        # Sort sod values
        self.SOD = {
            k: v
            for k, v in sorted(self.SOD.items(), key=lambda item: item[1], reverse=True)
        }
        log("computing SOD finished")

        # Save sod distribution in file e.g. for creating histograms
        file = open("sod.txt", "w")
        file.write(str(list(self.SOD.values())))
        file.close()
