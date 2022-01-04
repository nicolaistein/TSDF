import igl
import numpy as np
import os


class LSCM:
    def __init__(self, objPath):
        self.objPath = objPath

    def execute(self):
        root_folder = os.getcwd()

        # Load a mesh in OFF format
        v, f = igl.read_triangle_mesh(os.path.join(root_folder, self.objPath))
        print("Vertices: " + str(len(v)))
        print("Faces: " + str(len(f)))

        # Fix two points on the boundary
        b = np.array([2, 1])

        bnd = igl.boundary_loop(f)
        print("Boundary loop length: " + str(len(bnd)))

        b[0] = bnd[0]
        b[1] = bnd[int(bnd.size / 2)]

        bc = np.array([[0.0, 0.0], [1.0, 0.0]])

        # LSCM parametrization
        _, uv = igl.lscm(v, f, b, bc)

        return uv
