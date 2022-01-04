from typing import List
import array
import numpy as np
import bisect
from data_parser import SegmentationParser
from plotter import plotFeatureDistance, plotCharts
from priority_queue import PriorityQueue

prefix = "[Charts] "

def log(msg:str):
    print(prefix + msg)

class Charts:
    def __init__(self, parser:SegmentationParser):
        self.parser = parser

    def computeCharts(self, features:List[int]):
        self.features = features
        self.computeFeatureDistance()
        self.expand_charts()
        log("expand charts finished")
        log("Epsilon: " + str(self.epsilon))
        ch = self.getCharts()
        log("Charts count: " + str(len(ch)))
        print([(key,val) for key, val in ch.items() if val > -1])
        plotCharts(self.parser.vertices, self.parser.faces, self.charts, ch.keys())
    #    plotFeatureDistance(self.parser.vertices, self.parser.faces, self.featureDistances)
    #    print(self.featureDistances)


    def expandEdge(self, feature:int, edge:int, distance:int):

        newEdges = []
        handledFaces = 0
        for face in self.parser.edgeToFaces[edge]:
            if self.featureDistances[face] != -1: continue
            self.featureDistances[face] = distance
            if distance > self.maxDistance: self.maxDistance = distance
            handledFaces += 1
            if distance > 3:
                self.lastExpanded[feature] = face
            newEdges.extend([e.idx() for e in self.parser.mesh.fe(self.parser.faceHandles[face]) if e.idx() != edge])
        
        self.featureBorders[feature].remove(edge)
        self.featureBorders[feature].extend(newEdges)
    #    log("expandEdge newEdges size: " + str(len(newEdges)) + ", handledFaces: " + str(handledFaces))

        return handledFaces

    def computeFeatureDistance(self):
        log("Computing feature distance")
        faceCount = len(self.parser.faces)
        self.featureDistances = {}
        self.featureBorders = [[]]*self.parser.edgeCount
        self.maxDistance = 0
        self.currentFeatureDistance = {}
        for f in self.features:
            self.featureBorders[f] = [f]
            self.currentFeatureDistance[f] = 0

        for index, _ in enumerate(self.parser.faces):
            self.featureDistances[index] = -1

        handledFaces = 0
        self.localMaxima = []
        self.lastExpanded = [-1]*self.parser.edgeCount

        while handledFaces < faceCount and len(self.currentFeatureDistance) > 0:
            log("new round, handled faces: " + str(handledFaces) + ", remaining features: " + str(len(self.currentFeatureDistance)))
            toRemove = []
            for feature, distance in self.currentFeatureDistance.items():
                expanded = False
                for edge in self.featureBorders[feature]:
                    
                    fc = self.expandEdge(feature, edge, distance)

                    handledFaces += fc
                    expanded = True if fc>0 else expanded
        #            log("expanded: " + str(expanded))

                self.currentFeatureDistance[feature] += 1
                if not expanded: toRemove.append(feature)
    #            else: print("feature was actually expanded")

        #    log("toRemove size: " + str(len(toRemove)))
            for f in toRemove:
                if self.lastExpanded[f] != -1: self.localMaxima.append(self.lastExpanded[f])
                del self.currentFeatureDistance[f]
            
        self.epsilon = self.maxDistance / 2.5
        log("MAXIMA COUNT: " + str(len(self.localMaxima)))
        log("while loop end")
        log("handled faces: " + str(handledFaces))
        log("faceCount: " + str(faceCount))
        log("current feature distance length: " + str(len(self.currentFeatureDistance)))

        # Fix not reachable faces
        for key, val in self.featureDistances.items():
            if val == -1:
                total = []
                for x in self.parser.mesh.ff(self.parser.faceHandles[key]):
                    v = self.featureDistances[x.idx()]
                    if v != -1: total.append(v)
                self.featureDistances[key] = int(round(sum(total) / len(total)))

    def getChartElements(self, face:int):
#        log("getChartElements of " + str(face))
        searched = [False] * len(self.parser.faces)
        elements = [face]
        toSearch = [self.chartOf(face)]
        while toSearch:
#            log("getChartElements toSearch size: " + str(len(toSearch)))
            currentChart = toSearch.pop()
            searched[currentChart] = True
            for index, val in enumerate(self.charts):
                if val == currentChart:
                    elements.append(index)
            #        if index != currentChart and not searched[index]:
            #            toSearch.append(index)

#        log("getChartElements of " + str(face) + ": count=" + str(len(elements)))
        return elements


    def max_dist(self, chart:int):
        max = 0
        for f in self.getChartElements(chart):
            if self.featureDistances[f] > max:
                max = self.featureDistances[f]
        return max


    def getOppositeFace(self, edge:int, face:int):
        faces = self.parser.edgeToFaces[edge]
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
        seedCount = 200
       
    #    foreach facet F where dist(F ) is a local maximum
    #    for index, (face, val) in enumerate(sortedFaces.items()):
        for index, face in enumerate(self.localMaxima):
            if index >= seedCount: break
    #        create a new chart with seed F
            self.charts[face] = face
    #        add the halfedges of F to Heap
            for e in self.parser.mesh.fe(self.parser.faceHandles[face]):
                heap.insert(face, e.idx())
    #    end // foreach

        log("initial charts")
        print(self.getCharts())
        counter = 0
    #   #Charts-growing phase
    #   while(Heap is not empty)
        while heap.size() > 0:
            counter += 1
            if counter % 5000 == 0: 
                log(str(counter) + " | heap size: " + str(heap.size()) + " | charted faces: "
                 + str(self.getChartedFaces()) + "/" + str(len(self.parser.faces)))
    #        halfedge h ← e ∈ Heap such that dist(e) is maximum
    #        remove h from Heap
    #        facet F ← facet(h)
          
            f, h = heap.pop()

    #        facet Fopp ← the opposite facet of F relative to h
            fopp = self.getOppositeFace(h, f)

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
    #            log("ELSE CALLED MEEEEEEEEEEEEEEEEEEEEEEEEEEEEP")

                if (self.chartOf(fopp) != self.chartOf(f)):
                    if self.max_dist(f) - dist[f] < self.epsilon:
                        if self.max_dist(fopp) - dist[f] < self.epsilon:
            #            merge chart(F ) and chart(Fopp)

            #                self.charts[fopp] = self.charts[f]
                            self.merge(f, fopp)
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
        log("Merge " + str(c1) + " - " + str(c2) + ", actual: " + str(chart1) + " - " + str(chart2))
        for index, val in enumerate(self.charts):
            if val == chart2: self.charts[index] = chart1

    def getCharts(self):
        map = {}
        for val in self.charts:
            if val not in map: map[val] = 0
            map[val] += 1

        return map
