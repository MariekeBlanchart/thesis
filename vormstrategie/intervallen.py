import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from gatefitness import gatefitness

##line termibalbuilsing
lineterminalpoint = (-3342.6912, 1041.9505)
linelength = 900
lineangle = 25

agate_min = None
agate_max = None
pgate_min = None
pgate_max = None

airport =None

def setairport (a):
    global airport
    airport = a
def initialvalue ():
    return 20*[0]

def setmeasures(minarea, maxarea, minperiphery, maxperiphery):
    global agate_min
    global agate_max
    global pgate_min
    global pgate_max
    agate_min = minarea
    agate_max = maxarea
    pgate_min = minperiphery
    pgate_max = maxperiphery

def construct(coords):
    polygons = []
    
    for i in range (0,10):
        x1 = 90*i 
        y1 = -coords[2*i]
        
        x2 =  90*i +90
        y2 = -coords[2*i]
        
        x3 = 90*i +90
        y3 = coords[2*i+1]
        
        x4 =  90*i
        y4 = coords[2*i+1]
        
        polygons.append(geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)]))

    polygon = polygons[0]
    for p in polygons[1:]:
        polygon = polygon.union(p)
    polygon = affinity.rotate(polygon, lineangle)
    polygon = affinity.translate(polygon, xoff=lineterminalpoint[0], yoff=lineterminalpoint[1], zoff=0.0)
    
    return polygon

def fitness(coords):

    return gatefitness(airport, construct(coords), agate_min, agate_max, pgate_min, pgate_max)

