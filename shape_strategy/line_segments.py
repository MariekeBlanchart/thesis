import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from shape_strategy.gate_fitness import gatefitness

airport =None

## elements line
maxsegments = 20


def setairport (a):
    global airport 
    airport = a
def initialvalue ():
    return [airport.centroid.coords[0][0], airport.centroid.coords[0][1]] + 5*[0] + maxsegments*[0]
def setmeasures(minarea, maxarea, minperiphery, maxperiphery):#, runwaypointsa):
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
    ## wich figure, form triangle -> octagon    
    figure = coords[2]
    if -4000 < figure <= -967.63:
        numbervertices= 3
    elif -967.63 < figure <= -430.383:
        numbervertices= 4
    elif -430.383 < figure <= 0:
        numbervertices= 5
    elif 0 < figure <= 430.108:
        numbervertices= 6
    elif 430.108 < figure  <= 967.23:
        numbervertices= 7
    elif  967.23 < figure <= 4000:
        numbervertices= 8
    else:
        return None
        
    ##
    
    lengthsides = []
    heights = []
    skip = 7
    for i in range (0,4):
        lengthsides.append(int(coords[3 +i ]/100))
        
        if lengthsides[i] < 0 or sum(lengthsides) > maxsegments:
            return None
        
        heights.append([])
        for numberheight in range (0, lengthsides[i]):
            heights[i].append(int(coords[skip + numberheight]/145))
        skip = skip + lengthsides [i]
        

    points = []
    
    x = coords[0]
    y = coords[1]
    angle = 0
    length_segment = 90
    
    for side in range (0, numbervertices):
        if numbervertices%2 == 1:
            lengthside = lengthsides[0]
            sideheights = heights[0]
        else:
            lengthside = lengthsides[side % (numbervertices/2)]
            sideheights = heights[side % (numbervertices/2)]
    
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
            
        angle += 360/ numbervertices
        
    try:
        polygon = geometry.Polygon(points)
    except:
        polygon = None
        
    return polygon

def fitness(coords):
    
    errors = 0
    
    for c in coords[7:]:
        if c < 0:
            errors += 10000000 - 10000*c
        if c >= 7 * 145:
            errors += 10000*c  
    
    if coords[2] <= -4000:
        errors += 100000000 - 10000*coords[2]
    elif coords[2] > 4000:
        errors += 100000000 + 10000*coords[2]
    
    lengthsides = []
    for i in range (0,4):
        lengthsides.append(int(coords[3 +i ]/100))
        
        if lengthsides[i] <= 0:
            errors += 10000000 - 10000*lengthsides[i]
        
    if sum(lengthsides) > maxsegments:
        errors += 100000000 + 10000*sum(lengthsides)
     
    if errors:
        return errors
    
    return gatefitness(airport, construct(coords),agate_min, agate_max, pgate_min, pgate_max)

def printline(coords):
    ## wich figure, form triangle -> octagon    
    figure = coords[2]
    if -4000 < figure <= -967.63:
        numbervertices= 3
    elif -967.63 < figure <= -430.383:
        numbervertices= 4
    elif -430.383 < figure <= 0:
        numbervertices= 5
    elif 0 < figure <= 430.108:
        numbervertices= 6
    elif 430.108 < figure  <= 967.23:
        numbervertices= 7
    elif  967.23 < figure <= 4000:
        numbervertices= 8
    else:
        return None
    print('Aantal hoeken van figuur:     ' + str(numbervertices))

