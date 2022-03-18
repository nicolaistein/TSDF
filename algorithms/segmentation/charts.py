from typing import List
from algorithms.segmentation.data_parser import SegmentationParser
from algorithms.segmentation.plotter import plotFeatureDistance, plotCharts
from algorithms.segmentation.priority_queue import PriorityQueue
from algorithms.segmentation.parameters import *
from logger import log
from util import faceToArea


class Charts:
    def __init__(self, parser: SegmentationParser, maxChartCount: int):
        self.parser = parser
        self.maxChartCount = maxChartCount

    def plotCurrentFeatureDistance(self):
        plotFeatureDistance(
            self.parser.vertices, self.parser.faces, self.featureDistances
        )

    def plotCurrentCharts(self, folder: str = None):
        ch = self.getCharts()
        plotCharts(
            self.parser.vertices, self.parser.faces, self.charts, ch.keys(), folder
        )

    def computeCharts(self, features: List[int]):
        self.features = features
        self.computeFeatureDistance()
        self.plotCurrentFeatureDistance()
        self.expand_charts()
        self.fixUnchartedFaces()
        self.removeSmallChartsNew()
        ch = self.getCharts()
        return self.charts, ch.keys()

    def getBorderCharts(self, face: int, chart: int):
        result = []
        for edge in self.parser.mesh.fe(self.parser.faceHandles[face]):
            edgeId = edge.idx()
            oppFace = self.getOppositeFace(edgeId, face)
            oppChart = self.charts[oppFace]
            if oppFace == -1 or oppChart == chart:
                continue
            result.append((oppChart, self.parser.SOD[edgeId]))

        return result

    def removeChart(self, chart: int):
        chartsBefore = self.getCharts()

        borderChartCount = {}
        borderSod = {}
        for index, ic in enumerate(self.charts):
            if ic == chart:
                for chartRes, sod in self.getBorderCharts(index, chart):
                    if chartRes not in borderChartCount:
                        borderChartCount[chartRes] = 0
                        borderSod[chartRes] = 0

                    borderChartCount[chartRes] += 1
                    borderSod[chartRes] += sod

        evaluation = {}
        for borderChart, borderCount in borderChartCount.items():
            evaluation[borderChart] = borderSod[borderChart] / borderCount

        k = list(evaluation.keys())
        v = list(evaluation.values())

        if len(v) == 0:
            log("Error: Aborted chart deletion because no neighbor could be found")
            return

        maxValue = min(v)
        largestNeighborId = k[v.index(maxValue)]
        for index, val in enumerate(self.charts):
            if val == chart:
                self.charts[index] = largestNeighborId

        chartsAfter = self.getCharts()
        diff = {}
        for key, val in chartsBefore.items():
            if key not in chartsAfter:
                diff[key] = val
            elif chartsAfter[key] != val:
                diff[key] = chartsAfter[key] - val

        return largestNeighborId

    def getAreaOfChart(self, chart: int):
        res = 0
        for index, val in enumerate(self.charts):
            if val == chart or chart == -1:
                res += faceToArea(self.parser.faces[index], self.parser.vertices)

        return res

    def removeSmallChartsNew(self):
        log("Removing small charts")
        ch = self.getCharts()
        print(ch)
        min = self.getAreaOfChart(-1) * minChartSizeFactor

        chartAreas = {}
        for key, val in ch.items():
            area = self.getAreaOfChart(key)
            chartAreas[key] = area

        sortedCharts = {
            k: v for k, v in sorted(chartAreas.items(), key=lambda item: item[1])
        }

        while True:
            if len(self.getCharts()) <= self.maxChartCount:
                break
            chart = list(sortedCharts.keys())[0]
            longest = self.removeChart(chart)
            chartAreas[longest] = self.getAreaOfChart(longest)
            chartAreas.pop(chart, None)
            sortedCharts = {
                k: v for k, v in sorted(chartAreas.items(), key=lambda item: item[1])
            }

    def getNeighborSOD(self, chart1: int, chart2: int):
        totalSOD = 0
        edgeCount = 0

        for index, val in enumerate(self.charts):
            if val != chart1:
                continue
            face = index
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                edge = e.idx()
                oppFace = self.getOppositeFace(edge, face)
                if oppFace != -1 and self.charts[oppFace] == chart2:
                    edgeCount += 1
                    totalSOD += self.parser.SOD[edge]

        if edgeCount == 0:
            return -1
        return totalSOD / edgeCount

    def fixUnchartedFaces(self):
        log("Fixing uncharted faces")
        found = []
        for key, val in enumerate(self.charts):
            if val == -1:
                found.append(key)

        log("Uncharted faces size: " + str(len(found)))
        unprocessed = 0
        while len(found) > 0:
            face = found.pop(0)
            adjacent = []
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                edge = e.idx()
                oppFace = self.getOppositeFace(edge, face)
                oppChart = self.charts[oppFace]
                if oppFace != -1 and oppChart != -1:
                    adjacent.append((self.parser.SOD[edge], oppChart))

            if len(adjacent) == 0:
                found.append(face)
                unprocessed += 1
                continue

            if len(adjacent) < 2 and unprocessed < len(found) - 1:
                found.append(face)
                unprocessed += 1
                continue

            minChart = -1
            minValue = 10000000000000

            for sod, oppChart in adjacent:
                if sod < minValue:
                    minValue = sod
                    minChart = oppChart

            self.charts[face] = minChart
            unprocessed = 0
            if len(found) % 400 == 0:
                log("Remaining: " + str(len(found)))

    def expandEdge(self, feature: int, edge: int, distance: int):
        newEdges = []
        handledFaces = 0
        for face in self.parser.edgeToFaces[edge]:
            if self.featureDistances[face] != -1:
                continue
            self.featureDistances[face] = distance
            if distance > self.maxDistance:
                self.maxDistance = distance
            handledFaces += 1
            if distance >= seedMinFeatureDistance:
                self.lastExpanded[feature] = face
            newEdges.extend(
                [
                    e.idx()
                    for e in self.parser.mesh.fe(self.parser.faceHandles[face])
                    if e.idx() != edge
                ]
            )

        self.featureBorders[feature].remove(edge)
        self.featureBorders[feature].extend(newEdges)

        return handledFaces

    def computeFeatureDistance(self):
        log("Computing feature distance")
        faceCount = len(self.parser.faces)
        self.featureDistances = {}
        self.featureBorders = [[]] * self.parser.edgeCount
        self.maxDistance = 0
        self.currentFeatureDistance = {}
        for index, f in enumerate(self.features):
            if f:
                self.featureBorders[index] = [index]
                self.currentFeatureDistance[index] = 0

        for index, _ in enumerate(self.parser.faces):
            self.featureDistances[index] = -1

        handledFaces = 0
        self.localMaxima = []
        self.lastExpanded = [-1] * self.parser.edgeCount

        while handledFaces < faceCount and len(self.currentFeatureDistance) > 0:
            toRemove = []
            for feature, distance in self.currentFeatureDistance.items():
                expanded = False
                for edge in self.featureBorders[feature]:

                    fc = self.expandEdge(feature, edge, distance)

                    handledFaces += fc
                    if fc > 0:
                        expanded = True

                self.currentFeatureDistance[feature] += 1
                if not expanded:
                    toRemove.append(feature)

            for f in toRemove:
                if self.lastExpanded[f] != -1:
                    self.localMaxima.append(self.lastExpanded[f])
                del self.currentFeatureDistance[f]

        self.epsilon = self.maxDistance * epsilonFactor
        log("local maxima: " + str(len(self.localMaxima)))

        # Fix not reachable faces
        repeat = False
        repeatCounter = 0
        missingCounter = 0
        while True:
            repeatCounter += 1
            repeat = False
            for key, val in self.featureDistances.items():
                if val == -1:
                    missingCounter += 1
                    total = []
                    for x in self.parser.mesh.ff(self.parser.faceHandles[key]):
                        v = self.featureDistances[x.idx()]
                        if v != -1:
                            total.append(v)

                    # Todo: HERE
                    if len(total) != 0:
                        self.featureDistances[key] = int(round(sum(total) / len(total)))
                    else:
                        repeat = True

            if not repeat:
                break

        log("repeatCounter: " + str(repeatCounter))
        log("missingCounter: " + str(missingCounter))

    def getChartElements(self, face: int):
        searched = [False] * len(self.parser.faces)
        elements = [face]
        toSearch = [self.chartOf(face)]
        while toSearch:
            currentChart = toSearch.pop()
            searched[currentChart] = True
            for index, val in enumerate(self.charts):
                if val == currentChart:
                    elements.append(index)

        return elements

    def max_dist(self, chart: int):
        max = 0
        for f in self.getChartElements(chart):
            if self.featureDistances[f] > max:
                max = self.featureDistances[f]
        return max

    def getOppositeFace(self, edge: int, face: int, shouldLog: bool = False):
        faces = self.parser.edgeToFaces[edge]

        toPrint = []
        for k in faces:
            toPrint.append(self.charts[k])
        if shouldLog:
            log("Charts of edge " + str(edge) + ": " + str(toPrint))
        if len(faces) == 1:
            return -1
        return faces[0] if faces[0] != face else faces[1]

    def chartOf(self, face: int):
        if self.charts[face] == -1:
            return -1
        current = face
        while current != self.charts[current] and current != -1:
            current = self.charts[current]

        return current

    def expand_charts(self):
        dist = self.featureDistances
        self.charts = [-1] * len(self.parser.faces)

        heap = PriorityQueue(self.featureDistances)
        chart_boundaries = [True] * self.parser.edgeCount

        for index, face in enumerate(self.localMaxima):
            self.charts[face] = face
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                heap.insert(face, e.idx())

        self.plotCurrentCharts()
        counter = 0
        while heap.size() > 0:
            counter += 1
            if counter % 5000 == 0:
                log(
                    str(counter)
                    + " | heap size: "
                    + str(heap.size())
                    + " | charted faces: "
                    + str(self.getChartedFaces())
                    + "/"
                    + str(len(self.parser.faces))
                )

            f, h = heap.pop()
            fopp = self.getOppositeFace(h, f)

            if fopp == -1:
                continue

            # --------------------------------------------------------
            if self.parser.SOD[h] > maxSOD:
                continue
            # --------------------------------------------------------

            if self.chartOf(fopp) == -1:
                self.charts[fopp] = self.charts[f]
                chart_boundaries[h] = False
                chart_boundaries = self.removeNonExtremalEdges(chart_boundaries, h)
                for eh in self.parser.mesh.fe(self.parser.faceHandles[fopp]):
                    id = eh.idx()
                    if chart_boundaries[id]:
                        heap.insert(fopp, id)
            else:
                if self.chartOf(fopp) != self.chartOf(f):
                    if self.max_dist(f) - dist[f] < self.epsilon:
                        if self.max_dist(fopp) - dist[f] < self.epsilon:
                            self.merge(f, fopp)
                            pass

    def getChartedFaces(self):
        count = 0
        for val in self.charts:
            if val != -1:
                count += 1
        return count

    def removeNonExtremalEdges(self, chartBoundaries: List[bool], removedEdge: int):
        toSearch = [removedEdge]
        while toSearch:
            currentEdge = toSearch.pop()

            for vertex in self.parser.edgeToVertices[currentEdge]:
                border = []
                for ve in self.parser.mesh.ve(self.parser.vertexHandles[vertex]):
                    id = ve.idx()
                    if id != currentEdge and chartBoundaries[id]:
                        border.append(id)

                if len(border) == 1:
                    chartBoundaries[border[0]] = False
                    toSearch.append(border[0])

        return chartBoundaries

    def merge(self, c1: int, c2: int):
        chart1 = self.chartOf(c1)
        chart2 = self.chartOf(c2)
        for index, val in enumerate(self.charts):
            if val == chart2:
                self.charts[index] = chart1

    def getCharts(self):
        map = {}
        for val in self.charts:
            if val not in map:
                map[val] = 0
            map[val] += 1

        return map
