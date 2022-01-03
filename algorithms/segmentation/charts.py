from typing import List
import array
from data_parser import SegmentationParser

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

    def computeFeatureDistance(self):
        log("Computing feature distance")
        faceCount = len(self.parser.faces)
        self.featureDistances = array.array('i',(-1,)*faceCount)
        handledFaces = 0
        while handledFaces < faceCount:
            log("handled faces: " + str(handledFaces))
            for feat in self.features:
                pass




    def expand_charts(self):

    #    priority_queue<halfedge> Heap sorted by dist(facet(half edge))
    #    set<edge> chart_boundaries initialized with all the edges of the surface

    #    #Initialize Heap
    #    foreach facet F where dist(F ) is a local maximum
    #        create a new chart with seed F
    #        add the halfedges of F to Heap
    #    end // foreach

    #   #Charts-growing phase
    #   while(Heap is not empty)
    #        halfedge h ← e ∈ Heap such that dist(e) is maximum
    #        remove h from Heap
    #        facet F ← facet(h)
    #        facet Fopp ← the opposite facet of F relative to h

    #        if ( chart(Fopp) is undefined ) then
    #            add Fopp to chart(F )
    #            remove E from chart_boundaries
    #            remove non-extremal edges from chart_boundaries,
    #            #(i.e. edges that do not link two other chart boundary edges)
    #            add the halfedges of Fopp belonging to
    #            chart_boundaries to Heap

    #        elseif ( chart(Fopp) 6= chart(F ) and
    #            max_dist(chart(F )) - dist(F ) < ε and
    #            max_dist(chart(Fopp)) - dist(F ) < ε ) then
    #            merge chart(F ) and chart(Fopp)
    #        end // if
    #    end // while
        pass