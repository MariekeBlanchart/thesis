import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from gatefitness import gatefitness

airport =None

## elements line
maxsegments = 24
numbervertices= 4

def setairport (a):
    global airport 
    airport = a
def initialvalue ():
    return [airport.centroid.coords[0][0], airport.centroid.coords[0][1]] + 4*[0] + maxsegments*[0]
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
    ## wich figure, form triangle -> octagon    

    lengthsides = []
    skip = 6
    for i in range (0,4):
        lengthsides.append(int(coords[3 +i ]/100))
        
        if lengthsides[i] <= 0:
            return None
    
    if hastoomanysegments(lengthsides):
        return None

    points = []
    
    x = coords[0]
    y = coords[1]
    angle = 0
    length_segment = 90
    
    for side in range (0, numbervertices):
        if numbervertices%2 == 1:
            lengthside = lengthsides[0]
        else:
            lengthside = lengthsides[side % (numbervertices/2)]

        sideheights = []
        for numberheight in range (0, lengthside):
            sideheights.append(int(coords[skip + numberheight]/145))
        skip = skip + lengthside
    
        for i in range(0, lengthside):
            heightsegment = length_segment*sideheights [i]
            if i > 0:
                heightsegment -= length_segment*sideheights [i - 1]
            
            x += heightsegment * math.cos(math.radians(angle +90))
            y += heightsegment * math.sin(math.radians(angle +90))
            points.append((x, y))
            
            x += length_segment * math.cos(math.radians(angle))
            y += length_segment * math.sin(math.radians(angle))
            points.append((x, y))

        heightsegment = -length_segment*sideheights [lengthside - 1]
        
        x += heightsegment * math.cos(math.radians(angle +90))
        y += heightsegment * math.sin(math.radians(angle +90))
        points.append((x, y))
            
        angle += 360/ numbervertices
        
    try:
        polygon = geometry.Polygon(points)
    except:
        polygon = None
        
    return polygon

def fitness(coords):
    
    errors = 0
    
    for c in coords[6:]:
        if c < 0:
            errors += 1000000000 - 10000*c
        if c >= 7 * 145:
            errors += 10000*c  
            
    lengthsides = []
    for i in range (0,4):
        lengthsides.append(int(coords[3 +i ]/100))
        
        if lengthsides[i] <= 0:
            errors += 1000000 - 10000*lengthsides[i]
        
    if hastoomanysegments(lengthsides):
        errors += 1000000 + 10000*sum(lengthsides)
     
    if errors:
        return errors
    
    return gatefitness(airport, construct(coords),agate_min, agate_max, pgate_min, pgate_max)

def hastoomanysegments(lengthsides):
        if numbervertices%2 == 1:
            return lengthsides[0]*numbervertices > maxsegments
        else:
            needed = 0
            for i in range(0, numbervertices / 2):
                needed += 2*lengthsides[i]
            
            return needed > maxsegments

def printline(coords):
    print('Aantal hoeken van figuur:           ' + str(numbervertices))
