import math
from typing import List
from algorithms.segmentation.data_parser import SegmentationParser
from algorithms.segmentation.plotter import plotFeatureDistance, plotCharts
from algorithms.segmentation.priority_queue import PriorityQueue
from algorithms.segmentation.parameters import *
from logger import log
from util import faceToArea


class Charts:
    def __init__(self, parser:SegmentationParser, maxChartCount:int):
        self.parser = parser
        self.maxChartCount = maxChartCount

    def plotCurrentFeatureDistance(self):
        plotFeatureDistance(self.parser.vertices, self.parser.faces, self.featureDistances)


    def plotCurrentCharts(self, folder:str=None):
        ch = self.getCharts()
        plotCharts(self.parser.vertices, self.parser.faces, self.charts, ch.keys(), folder)

    def computeCharts(self, features:List[int]):
        self.features = features
        self.computeFeatureDistance()
#        self.plotCurrentFeatureDistance()

        self.expand_charts()
#        self.plotCurrentCharts()

        self.fixUnchartedFaces()
#        self.plotCurrentCharts()

#        self.removeSmallCharts()
        self.removeSmallChartsNew()
#        self.mergeFlatNeighbors()
        log("expand charts finished")
        log("Epsilon: " + str(self.epsilon))
        ch = self.getCharts()
        log("Charts count: " + str(len(ch)))
        print([(key,val) for key, val in ch.items() if val > -1])
    #    plotCharts(self.parser.vertices, self.parser.faces, self.charts, ch.keys())
    #    print(self.featureDistances)

        return self.charts, ch.keys()

    def getBorderCharts(self, face:int, chart:int):
        result = []
        for edge in self.parser.mesh.fe(self.parser.faceHandles[face]):
            edgeId = edge.idx()
            oppFace = self.getOppositeFace(edgeId, face)
            oppChart = self.charts[oppFace]
            if oppFace == -1 or oppChart == chart: continue
            result.append((oppChart, self.parser.SOD[edgeId]))

   #     log("result: " + str(result))
        return result

    def removeChart(self, chart:int):
#        if chart != 696: return
#        log("Removing chart " + str(chart))
        chartsBefore = self.getCharts()

        # chart => number of faces of this chart that are next to the currentChart
        borderChartCount = {}
        # chart => total sod count of the border edges which separate chart and the currentChart
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
#        log("max: " + str(maxValue))
#        log("largestNeighborId: " + str(largestNeighborId))
        for index, val in enumerate(self.charts):
            if val == chart: self.charts[index] = largestNeighborId

        
        
        chartsAfter = self.getCharts()
        diff = {}
        for key, val in chartsBefore.items():
            if key not in chartsAfter: 
                diff[key] = val
            elif chartsAfter[key] != val:
                diff[key] = chartsAfter[key]-val
#        log("Charts after: " + str(chartsAfter))
#        log("Differences: " + str(diff))

        return largestNeighborId


    def getAreaOfChart(self, chart:int):
        res = 0
        for index, val in enumerate(self.charts):
            if val == chart or chart == -1: 
                res += faceToArea(self.parser.faces[index], self.parser.vertices)

    #    log("chart: " + str(chart) + " => " + str(res))
        return res

    def removeSmallChartsNew(self):
        log("Removing small charts")
        ch = self.getCharts()
        print(ch)

#        min = len(self.parser.faces)*minChartSizeFactor
        min = self.getAreaOfChart(-1)*minChartSizeFactor
#        log("removeSmallCharts min: " + str(min))

        chartAreas = {}
        for key, val in ch.items():
            area = self.getAreaOfChart(key)
            chartAreas[key] = area

        sortedCharts = {k: v for k, v in sorted(chartAreas.items(), key=lambda item: item[1])}
#        log("sortedCharts: " + str(sortedCharts))

        while True:
            if len(self.getCharts()) <= self.maxChartCount: break
            chart = list(sortedCharts.keys())[0]
            longest = self.removeChart(chart)
            chartAreas[longest] = self.getAreaOfChart(longest)
            chartAreas.pop(chart, None)
            sortedCharts = {k: v for k, v in sorted(chartAreas.items(), key=lambda item: item[1])}


    def removeSmallCharts(self):
        log("Removing small charts")
        ch = self.getCharts()
        print(ch)

#        min = len(self.parser.faces)*minChartSizeFactor
        min = self.getAreaOfChart(-1)*minChartSizeFactor
#        log("removeSmallCharts min: " + str(min))
        toRemove = []
        for key, val in ch.items():
            area = self.getAreaOfChart(key)
            if area <= min:
                toRemove.append((key, area))

        
        sortedRemove = sorted(toRemove, key=lambda tup: tup[1])

#        log("toRemove: " + str(sortedRemove))

        for chart, _ in sortedRemove:
            self.removeChart(chart)

    def getNeighborSOD(self, chart1:int, chart2:int):
        totalSOD = 0
        edgeCount = 0

        for index, val in enumerate(self.charts):
            if val != chart1: continue
            face = index
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                edge = e.idx()
                oppFace = self.getOppositeFace(edge, face)
                if oppFace != -1:
                    edgeCount += 1
                    totalSOD += self.parser.SOD[edge]

        return totalSOD/edgeCount


    def mergeFlatNeighbors(self):
#        neighborSODs = {}
        nextLoop = True
        while(nextLoop):
#            log("entering next mainLoop")
            nextLoop = False
            #Compute avg SOD of all neighbors
            charts = self.getCharts()
            for c in charts:
                if nextLoop:continue
                for c2 in charts:
                    if nextLoop:continue
                    if c != c2:
                        sod = self.getNeighborSOD(c, c2)
                        if not math.isnan(sod):
 #                           log("sod: " + str(sod) + ", mergingUpToSOD: " + str(mergingUpToSOD))
                            if sod < mergingUpToSOD:
                                self.merge(c, c2)
                                nextLoop = True
#                                log("Merging " + str(c) + " and " + str(c2))


            # When somewhere below mergingUpToSOD
                # Merge
            
            if not nextLoop: 
                break
            

    def fixUnchartedFaces(self):
        log("Fixing uncharted faces")
#        chartsBefore = self.getCharts()
        found = []
        for key, val in enumerate(self.charts):
            if val == -1: found.append(key)

        log("Uncharted faces size: " + str(len(found)))

        while len(found) > 0:

            face = found.pop(0)
            adjacent = []
#            neighbors = 0
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                edge = e.idx()
                oppFace = self.getOppositeFace(edge, face)
#                if oppFace != -1: neighbors += 1
                oppChart = self.charts[oppFace]
                if oppFace != -1 and oppChart != -1:
                    adjacent.append((self.parser.SOD[edge], oppChart))

            if len(adjacent) == 0:
                found.append(face)
                continue

#            if neighbors >= 2 and len(adjacent) <= 1:
#                found.append(face)
#                continue


            minChart = -1
            minValue = 10000000000000

            for sod, oppChart in adjacent:
                if sod < minValue:
                    minValue = sod
                    minChart = oppChart

            self.charts[face] = minChart
        

    def expandEdge(self, feature:int, edge:int, distance:int):

        newEdges = []
        handledFaces = 0
        for face in self.parser.edgeToFaces[edge]:
            if self.featureDistances[face] != -1: continue
            self.featureDistances[face] = distance
            if distance > self.maxDistance: self.maxDistance = distance
            handledFaces += 1
            if distance >= seedMinFeatureDistance:
                self.lastExpanded[feature] = face
            newEdges.extend([e.idx() for e in self.parser.mesh.fe(self.parser.faceHandles[face]) if e.idx() != edge])
        
        self.featureBorders[feature].remove(edge)
        self.featureBorders[feature].extend(newEdges)

        return handledFaces

    def computeFeatureDistance(self):
        log("Computing feature distance")
        faceCount = len(self.parser.faces)
        self.featureDistances = {}
        self.featureBorders = [[]]*self.parser.edgeCount
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
        self.lastExpanded = [-1]*self.parser.edgeCount

        while handledFaces < faceCount and len(self.currentFeatureDistance) > 0:
    #        if handledFaces / faceCount < 0.4:
    #            self.plotCurrentFeatureDistance()
    #        log(str(handledFaces*100/len(self.parser.faces)) + ", remaining features: " + str(len(self.currentFeatureDistance)))
            toRemove = []
            for feature, distance in self.currentFeatureDistance.items():
                expanded = False
    #            log("feature " + str(feature) + ": New round! expanded: " + str(expanded) + ", " + str(self.currentFeatureDistance))
                for edge in self.featureBorders[feature]:
                    
                    fc = self.expandEdge(feature, edge, distance)

                    handledFaces += fc
                    if fc>0: 
   #                     if not expanded: log("feature " + str(feature) + ": expanded changed to True")
                        expanded = True
                        
        #            log("expanded after: " + str(expanded) + ", fc: " + str(fc))

   #                 if not expanded: log("feature " + str(feature) + ": failed to expand: " + str(expanded))

                self.currentFeatureDistance[feature] += 1
                if not expanded: 
    #                log("feature " + str(feature) + ": ACTUALLY FAILED: " + str(expanded))
                    toRemove.append(feature)
    #            else: print("feature was actually expanded")

    #        if len(toRemove) > 0: log("Removing " + str(len(toRemove)) + " elements")

            for f in toRemove:
    #            log("removing " + str(f) + ", lastExpanded: " + str(self.lastExpanded[f]))
                if self.lastExpanded[f] != -1: self.localMaxima.append(self.lastExpanded[f])
                del self.currentFeatureDistance[f]
        

        self.epsilon = self.maxDistance * epsilonFactor
        

        log("local maxima: " + str(len(self.localMaxima)))
    #    log("while loop end")
    #    log("handled faces: " + str(handledFaces))
    #    log("faceCount: " + str(faceCount))
    #    log("current feature distance length: " + str(len(self.currentFeatureDistance)))

        # Fix not reachable faces
        repeat = False
        repeatCounter = 0
        missingCounter = 0
        while(True):
            repeatCounter += 1
            repeat = False
            for key, val in self.featureDistances.items():
                if val == -1:
                    missingCounter += 1
                    total = []
                    for x in self.parser.mesh.ff(self.parser.faceHandles[key]):
                        v = self.featureDistances[x.idx()]
                        if v != -1: total.append(v)

                    # Todo: HERE
                    if len(total) != 0:
                        self.featureDistances[key] = int(round(sum(total) / len(total)))
                    else:
 #                       log("Repeat = True")
                        repeat = True
            
            if not repeat: break

        log("repeatCounter: " + str(repeatCounter))
        log("missingCounter: " + str(missingCounter))

    def getChartElements(self, face:int):
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


    def max_dist(self, chart:int):
        max = 0
        for f in self.getChartElements(chart):
            if self.featureDistances[f] > max:
                max = self.featureDistances[f]
        return max


    def getOppositeFace(self, edge:int, face:int, shouldLog:bool=False):
        faces = self.parser.edgeToFaces[edge]

        toPrint = []
        for k in faces:
            toPrint.append(self.charts[k])
        if shouldLog: log("Charts of edge " + str(edge) + ": " + str(toPrint))
        if len(faces) == 1: return -1
        return faces[0] if faces[0]!=face else faces[1]

    def chartOf(self, face:int):
    #    log("chartOf " + str(face))
        if self.charts[face] == -1: return -1
        current = face
        while current != self.charts[current] and current != -1:
            current = self.charts[current]

    #    log("chartOf " + str(face) + " is " + str(current))
        return current

    def expand_charts(self):
        dist = self.featureDistances
        self.charts = [-1] * len(self.parser.faces)
        
    #    priority_queue<halfedge> Heap sorted by dist(facet(half edge))
        heap = PriorityQueue(self.featureDistances)

    #    set<edge> chart_boundaries initialized with all the edges of the surface
        chart_boundaries = [True] * self.parser.edgeCount

    #    #Initialize Heap  
        sortedFaces = {k: v for k, v in sorted(self.featureDistances.items(), key=lambda item: item[1], reverse=True)}

       
    #    foreach facet F where dist(F ) is a local maximum
    #    for index, (face, val) in enumerate(sortedFaces.items()):

        for index, face in enumerate(self.localMaxima):
            if index >= localMaximumSeedCount: break
    #        create a new chart with seed F
            self.charts[face] = face
    #        add the halfedges of F to Heap
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                heap.insert(face, e.idx())


        for index, (face, val) in enumerate(sortedFaces.items()):
            if index >= globalMaximumSeedCount: break
            self.charts[face] = face
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                heap.insert(face, e.idx())
    #    end // foreach
    #    self.plotCurrentCharts()
    #    log("initial charts")
    #    print(self.getCharts())
        counter = 0
    #   #Charts-growing phase
    #   while(Heap is not empty)
        while heap.size() > 0:
            counter += 1
            if counter % 5000 == 0: 
                log(str(counter) + " | heap size: " + str(heap.size()) + " | charted faces: "
                 + str(self.getChartedFaces()) + "/" + str(len(self.parser.faces)))
    #        if counter % 10000 == 0: self.plotCurrent()
    #        halfedge h ← e ∈ Heap such that dist(e) is maximum
    #        remove h from Heap
    #        facet F ← facet(h)
          
            f, h = heap.pop()
            if h in self.features: continue

    #        facet Fopp ← the opposite facet of F relative to h
            fopp = self.getOppositeFace(h, f)

            # Opposite face does not exist (edge part of boundary loop)
            if fopp == -1: continue

            # Do not go beyond features
            if self.features[h] and featureBarrier: continue
            if self.parser.SOD[h] > maxSOD: continue

    #        if ( chart(Fopp) is undefined ) then
            if self.chartOf(fopp) == -1:
    #            add Fopp to chart(F)
                self.charts[fopp] = self.charts[f]
    #            remove E from chart_boundaries
                chart_boundaries[h] = False

    #            remove non-extremal edges from chart_boundaries,
    #            #(i.e. edges that do not link two other chart boundary edges)
                chart_boundaries = self.removeNonExtremalEdges(chart_boundaries, h)

    #            add the halfedges of Fopp belonging to
    #            chart_boundaries to Heap
                for eh in self.parser.mesh.fe(self.parser.faceHandles[fopp]):
                    id = eh.idx()
                    if chart_boundaries[id]: heap.insert(fopp, id)

    #        elseif ( chart(Fopp) != chart(F ) and
#            max_dist(chart(F )) - dist(F ) < ε and
#            max_dist(chart(Fopp)) - dist(F ) < ε ) then
            else:

                if (self.chartOf(fopp) != self.chartOf(f)):
                    if self.max_dist(f) - dist[f] < self.epsilon:
                        if self.max_dist(fopp) - dist[f] < self.epsilon:
            #            merge chart(F ) and chart(Fopp)

            #                self.charts[fopp] = self.charts[f]
                            self.merge(f, fopp)
            #                log("Potential Merge")
                            pass
    #        end // if
    #    end // while


    def getChartedFaces(self):
        count = 0
        for val in self.charts:
            if val != -1: count += 1
        return count


    def removeNonExtremalEdges(self, chartBoundaries:List[bool], removedEdge:int):
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

    def merge(self, c1:int, c2:int):
        chart1 = self.chartOf(c1)
        chart2 = self.chartOf(c2)
#        log("Merge " + str(chart1) + " - " + str(chart2))
        for index, val in enumerate(self.charts):
            if val == chart2: self.charts[index] = chart1

    def getCharts(self):
        map = {}
        for val in self.charts:
            if val not in map: map[val] = 0
            map[val] += 1

        return map
