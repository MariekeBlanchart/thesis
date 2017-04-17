import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from gatefitness import gatefitness

airport =None

##line termibalbuilsing
lineterminalpoint = (-3342.6912, 1041.9505)
linelength = 1395
lineangle = 25

def setairport (a):
    global airport 
    airport = a
def initialvalue ():
    return 8*[0] 
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
    maxsegments = 5

    points = []
    
    startx = coords[0]
    starty = coords[1]
    length_segment = coords[2]/100
    
    for i in range(0, maxsegments):
        heightsegment = length_segment*(int(coords[3 + i]/145) - 2)
        points.append((startx + length_segment*i, starty + heightsegment))
        points.append((startx + length_segment*i + length_segment, starty + heightsegment))
        
    startx = startx + length_segment*maxsegments
    starty = starty + length_segment*(int(coords[3 + maxsegments - 1]/145) - 2)
    
    for i in range(0, maxsegments):
        heightsegment = length_segment*(int(coords[3 + i]/145) - 2)
        points.append((startx + heightsegment, starty - length_segment*i))
        points.append((startx + heightsegment, starty - length_segment*i - length_segment))
        
    startx = startx + length_segment*(int(coords[3 + maxsegments - 1]/145)  - 2)
    starty = starty - length_segment*maxsegments
    
    for i in range(0, maxsegments):
        heightsegment = length_segment*(int(coords[3 + i]/145) - 2)
        points.append((startx - length_segment * i, starty - heightsegment))
        points.append((startx - length_segment * i - length_segment, starty - heightsegment))
        
    startx = startx - length_segment*maxsegments
    starty = starty - length_segment*(int(coords[3 + maxsegments - 1]/145) - 2)
    
    for i in range(0, maxsegments):
        heightsegment = length_segment*(int(coords[3 + i]/145) - 2)
        points.append((startx - heightsegment, starty + length_segment * i))
        points.append((startx - heightsegment, starty + length_segment * i + length_segment))
    
    try:
        polygon = geometry.Polygon(points)
    except:
        polygon = None
        
    return polygon

def fitness(coords):
    
    errors = 0
    for c in coords[3:]:
        if c < 0:
            errors += 10000000 - 10000*c
        if c >= 7 * 145:
            errors += 10000*c       
    if errors:
        return errors
    
    return gatefitness(airport, construct(coords),agate_min, agate_max, pgate_min, pgate_max)
    
