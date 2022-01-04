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

def plotFeatureDistance(vertices:List[List[float]], faces:List[List[int]], featureDistances):
    vt = np.transpose(vertices)
    ft = np.transpose(faces)

    colors = ["green"]*len(featureDistances)
    for index, x in featureDistances.items(): 
        distortion = x/16
        if distortion > 1:
            distortion = 1

        distFac = 1-distortion
        colorFac = int(round(distFac * 255, 0))
        color = '#%02x%02x%02xff' % (255, colorFac, colorFac)

        if x == -1: color='#%02x%02x%02xff' % (0, 255, 0)

        colors[index] = color

    fig = go.Figure(data=[go.Mesh3d(x=vt[0], y=vt[1], z=vt[2], i=ft[0], j=ft[1], k=ft[2],
         color='lightpink', facecolor=colors, opacity=1)])
    offline.plot(fig, filename='faceColorPlot.html')


distinctColors = ["#808080", "#dcdcdc", "#556b2f", "#8b4513", "#228b22", "#483d8b", "#b8860b",
    "#008b8b", "#000080", "#9acd32", "#8fbc8f", "#800080", "#b03060", "#ff0000", "#ffff00",
    "#deb887", "#00ff00", "#8a2be2", "#00ff7f", "#dc143c", "#00ffff", "#00bfff", "#0000ff", "#ff7f50",
    "#ff00ff", "#1e90ff", "#dda0dd", "#90ee90", "#ff1493", "#7b68ee"]

def plotCharts(vertices:List[List[float]], faces:List[List[int]], charts, chartList):

    chartToColor = {}
    for index, val in enumerate(chartList):
        chartToColor[val] = distinctColors[index % len(distinctColors)]

    vt = np.transpose(vertices)
    ft = np.transpose(faces)

    colors = ["green"]*len(faces)
    for index, x in enumerate(charts): 
        color = chartToColor[x] + "ff"
#        if index == 15318: color = "#000000ff"
        colors[index] = color

    fig = go.Figure(data=[go.Mesh3d(x=vt[0], y=vt[1], z=vt[2], i=ft[0], j=ft[1], k=ft[2],
         color='lightpink', facecolor=colors, opacity=1)])
    offline.plot(fig, filename='chartPlot.html')
