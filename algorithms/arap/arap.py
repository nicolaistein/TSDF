import numpy as np
import os
import igl
from logger import log


class ARAP:
    def __init__(self, objPath):
        self.objPath = objPath

    def execute(self):
        root_folder = os.getcwd()

        v, f = igl.read_triangle_mesh(os.path.join(root_folder, self.objPath))
        log("Vertices: " + str(len(v)))
        log("Faces: " + str(len(f)))

        if len(f) > 0 and type(f[0]) is not np.ndarray:
            f = np.matrix([list(f)])

        bnd = igl.boundary_loop(f)
        log("Boundary loop length: " + str(len(bnd)))

        bnd_uv = igl.map_vertices_to_circle(v, bnd)

        uv = igl.harmonic_weights(v, f, bnd, bnd_uv, 1)

        arap = igl.ARAP(v, f, 2, np.zeros(0))
        uva = arap.solve(np.zeros((0, 0)), uv)

        return uva
