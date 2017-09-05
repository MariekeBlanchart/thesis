import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from shape_strategy.gate_fitness import gatefitness

##line termibalbuilsing
#lineterminalpoint = (-3342.6912, 1041.9505)
#linelength = 900
#lineangle = 25

segments = 10

airport =None

def setairport (a):
    global airport
    airport = a
def initialvalue ():
    return [airport.centroid.coords[0][0], airport.centroid.coords[0][1], 90] + segments*2 *[0]

def setmeasures(minarea, maxarea, minperiphery, maxperiphery):#,runwaypointsa):
    global agate_min
    global agate_max
    global pgate_min
    global pgate_max
    #global runwaypoints
    agate_min = minarea
    agate_max = maxarea
    pgate_min = minperiphery
    pgate_max = maxperiphery
    #runwaypoints = runwaypointsa

def construct(coords):
    lineterminalpoint = (coords[0], coords[1])
    lineangle = coords[2]/1000

    polygons = []
    
    for i in range (0,segments):
        x1 = 90*i 
        y1 = -coords[3+2*i]
        
        x2 =  90*i +90
        y2 = -coords[3+2*i]
        
        x3 = 90*i +90
        y3 = coords[3+2*i+1]
        
        x4 =  90*i
        y4 = coords[3+2*i+1]
        
        polygons.append(geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)]))

    polygon = polygons[0]
    for p in polygons[1:]:
        polygon = polygon.union(p)
    polygon = affinity.rotate(polygon, lineangle)
    polygon = affinity.translate(polygon, xoff=lineterminalpoint[0], yoff=lineterminalpoint[1], zoff=0.0)
    
    return polygon

def fitness(coords):
    sumofnegativenumbers = -sum([x - 10 for x in coords[3:] if x < 10 ])
    if sumofnegativenumbers > 0:
        return 100000000000 + sumofnegativenumbers * 1000
    
    return gatefitness(airport, construct(coords), agate_min, agate_max, pgate_min, pgate_max)
 #, runwaypoints)
def printline(result_vormstrategie):
    pass
    print('Coordinaat X:                ' + str(result_vormstrategie[0]))
    print('Coordinaat Y:                ' + str(result_vormstrategie[1]))
    print('Hoek:                        ' + str(result_vormstrategie[2]/100))

