from typing import List
import plotly.graph_objects as go
import plotly.offline as offline
import numpy as np
def testplot():
    pts = np.loadtxt(np.DataSource().open('https://raw.githubusercontent.com/plotly/datasets/master/mesh_dataset.txt'))
    x, y, z = pts.T

    fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, color='lightpink', opacity=0.50)])
    offline.plot(fig, filename='result.html')



def plot(vertices:List[List[float]], faces:List[List[int]], coloredVertices:List[int]):

    vt = np.transpose(vertices)
    ft = np.transpose(faces)

    colors = ["lightpink"] * len(vertices)
    for x in coloredVertices: colors[x] = "green"

    fig = go.Figure(data=[go.Mesh3d(x=vt[0], y=vt[1], z=vt[2], i=ft[0], j=ft[1], k=ft[2],
         color='lightpink', vertexcolor=colors, opacity=1)])
    offline.plot(fig, filename='plot.html')
