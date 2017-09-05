import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
from draw_runways_gatefield import draw
from draw_plots import draw_plots


pointrunways = [(-2943.6089, -13624.1852), (-1279.0553,-15244.9889)]

#airport Zaventem
airport = geometry.Polygon([(-3887.5338, -15111.0947), (-4667.0044, -15075.6949), (-5206.3351, -14823.9632), (-5351.9938, -14894.7628), (-5690.5518, -14894.7628), (-5812.5901, -14407.0326), (-3667.0351, -13434.6257), (-3493.8194, -13517.2251), (-1625.8886, -12201.2692), (-1134.4820, -12251.2332), (-847.9250, -12831.8033), (-847.9250, -13066.4173), (-903.6444, -13352.7258), (-748.1866, -13807.8867), (-1026.7836, -14002.7356), (-891.1957, -14196.6008), (-645.5707, -14024.8123), (-478.4202, -14263.8059), (-445.6536, -14794.6836), (-374.8073, -14762.2405), (-224.9005, -14519.1844), ( 322.1703, -14333.9870), ( 489.5638, -14333.9870), ( 764.9966, -14504.7204), ( 793.5264, -14594.9865), ( 772.9215, -14680.5018), ( 642.9524, -14739.0956), ( -56.8857, -14999.0798), (-329.0749, -15184.6179), (-428.2840, -15156.6601), (-512.2302, -15156.6601), (-558.0190, -15197.3260), (-608.9783, -15356.6108), (-717.7563, -15533.3608), (-888.8519, -15668.8285), (-1350.3456, -15856.8472), (-1439.2633, -15856.8472), (-1595.8319, -15830.0995), (-1643.0105, -15829.5983), (-1702.7810, -15850.8541), (-1756.4732, -15888.3048), (-1796.9956, -15977.3768), (-1938.2913, -16236.8780), (-2038.4792, -16403.9284), (-2132.0601, -16533.5514), (-2228.8904, -16486.1521), (-2270.4820, -16375.1211), (-2286.0788, -16297.2046), (-2375.5261, -16174.4249), (-2451.9431, -16094.9365), (-2503.2366, -16062.5136), (-2582.7940, -16042.6415), (-2885.8776, -16053.6926), (-3126.3924, -16045.1804), (-3232.6228, -16006.4314), (-3402.9289, -15802.5783), (-3429.9081, -15590.3015), (-3402.9620, -15480.0297), (-3345.6312, -15390.7386), (-3428.3508, -15015.4501), (-3887.5338, -15111.0947)]
)
## gatebuilding,  ratio between length and width
minairportfield = 2015472
ratiolb= 1.5
## terminalbuilding
agate_min = 185842
agate_max = (agate_min + (agate_min * 0.1))
pgate_min = 4890
pgate_max =pgate_min + (pgate_min * 0.1)
## runways
numrunways = 2
preferredangledegrees = [24,20]
preferredangle = []
for i in range(0, numrunways):
    preferredangle.append(1.0 * (preferredangledegrees[i] % 180) / 360 * 2*math.pi)

## runways
minrunwaylength = 3500
minrunwaywidth = 60
usedtogether = [[1],[0]]

## buffer between runway and gatefield
bufferbetweenrg = 125

printpreviousresult = None

def fitness(coords):
    res = 0
    errors = 0

##runways
    runwaypolygons = []
    for i in range(0,numrunways):
        if i < numrunways:
            isrunway = True
            isgate = False
        else:
            isrunway = False
            isgate = True
            
        x = pointrunways[i][0]
        y = pointrunways[i][1]
        if i == 0:
            length = coords[0]
            width = coords[1]
        else:
            length = 3500
            width = 60
        angle = preferredangle[i]
         
        if length <= 0.1:
            errors += 100000*(1-length)
        if width <= 0.1:
            errors += 100000*(1-width)
        
        if errors:
            continue
 
        x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
        y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
         
        x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
        y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
         
        x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
        y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
         
        x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
        y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
         
        polygon = geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)]).buffer(75)
        
        runwaypolygons.append(polygon)
             
        if not airport.contains(polygon):
            try:
                areaoutsideairport = polygon.difference(airport).area / polygon.area * 100 # Percent of terminal that's outside airport
            except:
                print "Error: (%d %d) (%d %d) (%d %d) (%d %d) %d %d" % (x1, y1, x2, y2, x3, y3, x4, y4, length, width)
            res += 100 * (10 + areaoutsideairport)
             
            if areaoutsideairport > 99:
                # Try to guide terminal towards airport
                res += 100 *airport.centroid.distance(polygon.centroid)
                #print('A=', res)
        
        if isrunway:     
            if length < minrunwaylength:
                res += (10 + minrunwaylength-length)
                #print('B=', res)
                
            if width < minrunwaywidth:
                res += (10 + minrunwaywidth-width)
                #print('C=', res)
                
            if width > minrunwaywidth*2:
                res += (10 - minrunwaywidth *2+width)
    
                
            angledifference = (preferredangle[i] - angle) % math.pi
            
            if angledifference < math.pi / 2:
                res += 100*angledifference 
                
                #print('D=', res)
                
            else:
                res += 100*(math.pi - angledifference) 
                #print('E=', res)
        else:
            if length* width < minairportfield:
                res += (10 + minairportfield - length * width)
            if length > ratiolb* width: 
                res += (10+ length -ratiolb* width)
            if width > ratiolb*length : 
                res += (10+ width -ratiolb*length)
            
                #print('F=', res)
                        
    if not errors:
        for i in range(0, numrunways):
            for j in usedtogether[i]:
                if runwaypolygons[i].intersects(runwaypolygons[j]):
                    res += (10 + runwaypolygons[i].intersection(runwaypolygons[j]).area)
                    #print('H=', res)           
                
    if errors:
        return errors
    
    return res
    
## Optimalisation
es = cma.CMAEvolutionStrategy(numrunways * [0], 1000)

logger = cma.CMADataLogger().register(es)
    
## Draw in in difrent filles
if printpreviousresult:
    result = printpreviousresult
else:
    es.optimize(fitness, logger=logger)
    es.result_pretty()
    result = es.result()[0]

print('Result: [' + ', '.join(map(str,result)) + ']')

steps = logger.load().data()["xrecent"]

i = 0
while i < len(steps):
    print("%d of %d" % (i + 1, len(steps)))
    print(steps[i][5:])
    draw(airport, [pointrunways[0][0], pointrunways[0][1], steps[i][5], steps[i][6] * 100, preferredangle[0] * 1000, pointrunways[1][0], pointrunways[1][1], 3500, 80*100, preferredangle[1] * 1000, 0, 0, 0, 0, 0], numrunways, filenamenum=i, ofnum=len(steps))
          
    i += 1

draw_plots([step[4] for step in steps])
draw(airport, [pointrunways[0][0], pointrunways[0][1], result[0], result[1] * 100, preferredangle[0] * 1000, pointrunways[1][0], pointrunways[1][1], 3500, 80*100, preferredangle[1] * 1000, 0, 0, 0, 0, 0], numrunways)


print('Result landingsbanen:         [' + ', '.join(map(str,result)) + ']')
print('Fitness landingsbanen:        ' + str(min([step[4] for step in steps])))
print('Afmeting landingsbaan 1:      ' + str(result[0]) + ' x ' + str(result[1]))