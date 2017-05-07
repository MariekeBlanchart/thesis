import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from gatefitness import gatefitness

airport =None

numgate = 5
mingatelength = 600
mingatewidth = 60

def setairport (a):
    global airport
    airport = a
def initialvalue ():
    return [mingatelength, mingatewidth*100] + numgate * [airport.centroid.coords[0][0], airport.centroid.coords[0][1], 0]
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
    gatepolygons= []
    
    length = coords[0]
    width = coords[1]/100
    
    for i in range(0, numgate):

        x = coords[i*3 + 0 + 2]
        y = coords[i*3 + 1 + 2]
        angle = coords[i*3 + 2 + 2]/1000
        
        x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
        y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
        
        x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
        y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
        
        x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
        y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
        
        x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
        y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
        
        polygon = geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])
        
        gatepolygons.append(polygon)
    return gatepolygons 
            
def fitness(coords):
    return gatefitness(airport, construct(coords),agate_min, agate_max, pgate_min, pgate_max)

def printline(result_vormstrategie):
    print('Lengte gategebouw:            ' + str(result_vormstrategie[0]))
    print('Breedte gategebouw:           ' + str(result_vormstrategie[1]/100))
