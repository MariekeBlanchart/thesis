import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from gatefitness import gatefitness

airport =None

def setairport (a):
    global airport
    airport = a
def initialvalue ():
    return [airport.centroid.coords[0][0], airport.centroid.coords[0][1]] + 12*[0]
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
    ## Dragon curve
    #axiom = "F"
    #rules = dict([("F", "FF+[+F-F-F]-[-F+F+F]")])
    #theta = math.pi/2
    
    ## Pythogoras tree
#     axiom = "0"
#     rules = dict([("1", "11"), ("0", "1[-0]+0")])
#     theta = math.pi/4
    
    ## random construction

    alphabet = ["[", "]", "+", "F", "-", "[", "]"]
    maxletters = 12
    theta = math.pi/4

    rule = ""
    
    for c in range(0, maxletters):
        rulenumber = int(coords[2 + c] / 145)
        if rulenumber < 0 or rulenumber >= 7:
            return None
        rule += alphabet[rulenumber]

    polygon = None
    [x, y] = coords[:2]
    l = 300
    w = 120
    
    angle = 0
    positions = []
    polygons = []
    
    ##print(rule)
    
    for char in rule:
        if char == "F" or char == "0" or char == "1":
            x1 = x - w * math.sin(angle) / 2
            y1 = y + w * math.cos(angle) / 2
            
            x2 = x + w * math.sin(angle) / 2
            y2 = y - w * math.cos(angle) / 2
            
            x3 = x + w * math.sin(angle) / 2 + l * math.cos(angle)
            y3 = y - w * math.cos(angle) / 2 + l * math.sin(angle)
            
            x4 = x - w * math.sin(angle) / 2 + l * math.cos(angle)
            y4 = y + w * math.cos(angle) / 2 + l * math.sin(angle)
            
            polygons.append(geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)]))
            
            x = x + l * math.cos(angle)
            y = y + l * math.sin(angle)
        elif char == "G":
            x = x + l * math.cos(angle)
            y = y + l * math.sin(angle)
        elif char == "+":
            angle += theta
        elif char == "-":
            angle -= theta
        elif char == "[":
            positions.append((x, y, angle))
        elif char == "]":
            if len(positions):
                (x, y, angle) = positions.pop()
    
    if len(polygons):
        polygon = polygons[0]
        for p in polygons[1:]:
            try:
                polygon = polygon.union(p)
            except:
                return None
    else:
        polygon = None
    
    return polygon
        
def fitness(coords):
    errors = 0
    
    for c in coords[2:]:
        if c < 0:
            errors += 10000000 - 10000*c
        if c > 7 * 145:
            errors += 10000*c
            
    if errors:
        return errors
    
    return gatefitness(airport, construct(coords),agate_min, agate_max, pgate_min, pgate_max)
