import numpy as np
import os
import igl


class ARAP:
    def __init__(self, objPath):
        self.objPath = objPath

    def execute(self):
        root_folder = os.getcwd()
        # meshplot.offline()

        # Load a mesh in OFF format
        v, f = igl.read_triangle_mesh(os.path.join(root_folder, self.objPath))
        print("Vertices: " + str(len(v)))
        print("Faces: " + str(len(f)))

        # Find the open boundary
        bnd = igl.boundary_loop(f)
        print("Boundary loop length: " + str(len(bnd)))

        # Map the boundary to a circle, preserving edge proportions
        bnd_uv = igl.map_vertices_to_circle(v, bnd)

        # Harmonic parametrization for the internal vertices
        uv = igl.harmonic_weights(v, f, bnd, bnd_uv, 1)

        arap = igl.ARAP(v, f, 2, np.zeros(0))
        uva = arap.solve(np.zeros((0, 0)), uv)

        return uva
