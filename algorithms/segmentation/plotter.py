from typing import List
import plotly.graph_objects as go
import plotly.offline as offline
import numpy as np
from logger import log


def removeGrid(fig):
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="",
                tickvals=[],
                backgroundcolor="rgb(200, 200, 230)",
                gridcolor="white",
                showbackground=False,
                zerolinecolor="white",
            ),
            yaxis=dict(
                title="",
                tickvals=[],
                backgroundcolor="rgb(230, 200,230)",
                gridcolor="white",
                showbackground=False,
                zerolinecolor="white",
            ),
            zaxis=dict(
                title="",
                tickvals=[],
                backgroundcolor="rgb(230, 230,200)",
                gridcolor="white",
                showbackground=False,
                zerolinecolor="white",
            ),
        ),
        margin=dict(r=10, l=10, b=10, t=10),
    )


def plotFeatures(
    vertices: List[List[float]], faces: List[List[int]], coloredVertices: List[int]
):

    vt = np.transpose(vertices)
    ft = np.transpose(faces)

    colors = ["lightpink"] * len(vertices)
    for x in coloredVertices:
        colors[x] = "green"

    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=vt[0],
                y=vt[1],
                z=vt[2],
                i=ft[0],
                j=ft[1],
                k=ft[2],
                color="lightpink",
                vertexcolor=colors,
                opacity=1,
            )
        ]
    )
    removeGrid(fig)
    offline.plot(fig, filename="FeaturePlot.html", auto_open=False)


def plotFeatureDistance(
    vertices: List[List[float]], faces: List[List[int]], featureDistances
):
    vt = np.transpose(vertices)
    ft = np.transpose(faces)

    colors = ["green"] * len(featureDistances)
    for index, x in featureDistances.items():
        distortion = x / 16
        if distortion > 1:
            distortion = 1

        distFac = 1 - distortion
        colorFac = int(round(distFac * 255, 0))
        color = "#%02x%02x%02xff" % (255, colorFac, colorFac)

        if x == -1:
            color = "#%02x%02x%02xff" % (0, 255, 0)

        colors[index] = color

    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=vt[0],
                y=vt[1],
                z=vt[2],
                i=ft[0],
                j=ft[1],
                k=ft[2],
                color="lightpink",
                facecolor=colors,
                opacity=1,
            )
        ]
    )
    removeGrid(fig)
    offline.plot(fig, filename="FeatureDistancePlot.html", auto_open=False)


distinctColors = [
    "#808080",
    "#556b2f",
    "#8b4513",
    "#228b22",
    "#483d8b",
    "#b8860b",
    "#008b8b",
    "#000080",
    "#9acd32",
    "#8fbc8f",
    "#800080",
    "#b03060",
    "#ff0000",
    "#deb887",
    "#00ff00",
    "#8a2be2",
    "#00ff7f",
    "#dc143c",
    "#00ffff",
    "#00bfff",
    "#0000ff",
    "#ff7f50",
    "#ff00ff",
    "#1e90ff",
    "#dda0dd",
    "#90ee90",
    "#ff1493",
    "#7b68ee",
]


def plotCharts(
    vertices: List[List[float]],
    faces: List[List[int]],
    charts,
    chartList,
    folder: str = None,
    filename: str = None,
):
    if folder is None:
        folder = ""
    else:
        folder += "/"

    chartToColor = {}
    for index, val in enumerate(chartList):
        chartToColor[val] = distinctColors[index % len(distinctColors)]
        if val == -1:
            log("Uncharted faces: " + str(chartToColor[val]))
            chartToColor[val] = "#ff1100"

    vt = np.transpose(vertices)
    ft = np.transpose(faces)

    colors = ["green"] * len(faces)
    for index, x in enumerate(charts):
        color = chartToColor[x] + "ff"
        colors[index] = color

    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=vt[0],
                y=vt[1],
                z=vt[2],
                i=ft[0],
                j=ft[1],
                k=ft[2],
                color="lightpink",
                facecolor=colors,
                opacity=1,
            )
        ]
    )
    removeGrid(fig)

    name = folder + "ChartPlot.html"
    log("Creating chart plot name: " + name)
    offline.plot(fig, filename=name, auto_open=False)


def plotFaceColors(
    vertices: List[List[float]], faces: List[List[int]], colors: List[str]
):

    vt = np.transpose(vertices)
    ft = np.transpose(faces)

    for index, x in enumerate(colors):
        if len(x) <= 7:
            colors[index] = x + "ff"

    fig = go.Figure(
        data=[
            go.Mesh3d(
                x=vt[0],
                y=vt[1],
                z=vt[2],
                i=ft[0],
                j=ft[1],
                k=ft[2],
                color="lightpink",
                facecolor=colors,
                opacity=1,
            )
        ]
    )
    removeGrid(fig)

    offline.plot(fig, filename="FaceColorPlot.html")
