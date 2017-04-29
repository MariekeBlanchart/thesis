import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from cmath import polar
from draw_runways_gatefield import draw
from draw_plots import draw_plots
#import vormstrategie.lijnstukken as vormstrategie


##airport zaventem
airport = geometry.Polygon([(-4175.9299,  543.2448), (-4955.4006,  578.6446), (-5494.7312,  830.3763), (-5640.3899,  759.5767), (-5978.9479,  759.5767), (-6100.9862, 1247.3069), (-3955.4312, 2219.7139), (-3782.2155, 2137.1144), (-2143.2504, 3291.7641), (-1914.2847, 3453.0703), (-1422.8781, 3403.1063), (-1136.3211, 2822.5362), (-1136.3211, 2587.9222), (-1192.0405, 2301.6137), (-1036.5827, 1846.4528), (-1315.1798, 1651.6039), (-1179.5918, 1457.7388), (-933.9668, 1629.5272), (-766.8164, 1390.5336), (-734.0497,  859.6560), (-663.2034,  892.0990), (-579.4244, 1027.9368), (-513.2966, 1135.1551), (-164.9863, 1253.0670), (  33.7742, 1320.3525), ( 201.1677, 1320.3525), ( 476.6005, 1149.6191), ( 505.1303, 1059.3530), ( 484.5254,  973.8377), ( 354.5562,  915.2439), (-345.2818,  655.2597), (-617.4710,  469.7216), (-716.6801,  497.6794), (-800.6263,  497.6794), (-846.4152,  457.0135), (-897.3744,  297.7288), (-1006.1524,  120.9787), (-1177.2480,  -14.4890), (-1509.7546, -149.9567), (-1638.7417, -202.5077), (-1727.6594, -202.5077), (-1884.2280, -175.7600), (-1931.4066, -175.2588), (-1991.1771, -196.5146), (-2044.8693, -233.9653), (-2085.3917, -323.0373), (-2226.6874, -582.5385), (-2326.8753, -749.5889), (-2420.4562, -879.2118), (-2517.2865, -831.8126), (-2558.8781, -720.7816), (-2574.4749, -642.8651), (-2663.9222, -520.0854), (-2740.3392, -440.5970), (-2791.6327, -408.1741), (-2871.1901, -388.3020), (-3174.2737, -399.3531), (-3414.7885, -390.8409), (-3521.0189, -352.0919), (-3691.3250, -148.2388), (-3718.3042,   64.0380), (-3691.3581,  174.3099), (-3634.0273,  263.6009), (-3716.7469,  638.8895), (-4175.9299,  543.2448)])
areaterminalbuilding = 250000
agate_min = 260186
agate_max =286205
pgate_min =5369
pgate_max =5906



printpreviousresult = None
#printpreviousresult_vormstrategie = [-2024.54823986, 717.542998757, -6419.56521739, 956.710824252, 312.387807216, 892.210905842, 227.751783793, 130.229125326]

## runways

minrunwaylength = 3500
minrunwaywidth = 60
numrunways = 2
preferredangledegrees = [25,25]
usedtogether = [[1],[0]]
preferredangle = []
for i in range(0, numrunways):
    preferredangle.append(1.0 * (preferredangledegrees[i] % 180) / 360 * 2*math.pi)

## gatebuilding
minairportfield = 2165753


def fitness(coords):
    res = 0
    errors = 0

##runways
    runwaypolygons = []
    for i in range(0,numrunways + 1):
        if i < numrunways:
            isrunway = True
            isgate = False
        else:
            isrunway = False
            isgate = True
            
        x = coords[i*5 + 0]
        y = coords[i*5 + 1]
        if isrunway:
            length = coords[i*5 + 2]
        else:
            length = coords[i*5 + 2]/10
        if isrunway:
            width = coords[i*5 + 3]/100
        else:
            width = coords[i*5 + 3]/10
        angle = coords[i*5 + 4]/1000
         
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
        
        if isrunway:
            runwaypolygons.append(polygon)
        else:
            gatelocationpolygon = polygon
             
        if not airport.contains(polygon):
            try:
                areaoutsideairport = 10 + polygon.difference(airport).area / polygon.area * 100 # Percent of terminal that's outside airport
            except:
                print "Error: (%d %d) (%d %d) (%d %d) (%d %d) %d %d" % (x1, y1, x2, y2, x3, y3, x4, y4, length, width)
            res += areaoutsideairport
             
            if areaoutsideairport > 99:
                # Try to guide terminal towards airport
                
                res += airport.centroid.distance(polygon.centroid)
                #print('A=', res)
        
        if isrunway:     
            if length < minrunwaylength:
                res += (10 + minrunwaylength-length)
                #print('B=', res)
                
            if width < minrunwaywidth:
                res += (10 + minrunwaywidth-width)
                #print('C=', res)
                
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
            if length > 2* width: 
                res += (10+ length -2* width)
            if width > 2*length : 
                res += (10+ width -2*length)
            
                #print('F=', res)
                        
    if not errors:
        ##
        if not geometry.MultiPolygon(runwaypolygons).convex_hull.contains(gatelocationpolygon):
            res +=(10+ 10000*gatelocationpolygon.difference(geometry.MultiPolygon(runwaypolygons).convex_hull).area/ gatelocationpolygon.area )
            
        for i in range(0, numrunways):
            if runwaypolygons[i].intersects(gatelocationpolygon):
                res += (10 + runwaypolygons[i].intersection(gatelocationpolygon).area)      
                #print('G=', res)
                
            for j in usedtogether[i]:
                if runwaypolygons[i].intersects(runwaypolygons[j]):
                    res += (10 + runwaypolygons[i].intersection(runwaypolygons[j]).area)
                    #print('H=', res)           
                
    if errors:
        return errors
    
    return res
    
## Optimalisation
es = cma.CMAEvolutionStrategy(numrunways * [airport.centroid.coords[0][0], airport.centroid.coords[0][1], minrunwaylength, minrunwaywidth*100, 0] + [airport.centroid.coords[0][0], airport.centroid.coords[0][1], 1000, 1000,0], 1000)

logger = cma.CMADataLogger().register(es)
    
## Draw in in difrent filles
if printpreviousresult:
    result = printpreviousresult
else:
    es.optimize(fitness, logger=logger)
    es.result_pretty()

    result = es.result()[0]

print('Result: [' + ', '.join(map(str,result)) + ']')
# 
# ##uit result haal je plaats voor gate. 
# coords= result[numrunways*5:]
# 
# x = coords[0]
# y = coords[1]
# length = coords[2]/10
# width = coords[3]/10
# angle = coords[4]/1000
# 
# x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
# y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
#  
# x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
# y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
#  
# x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
# y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
#  
# x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
# y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
#  
# gatebuilding_polygon = geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])
# 
# vormstrategie.setairport(gatebuilding_polygon)
# vormstrategie.setmeasures(agate_min, agate_max, pgate_min, pgate_max)
# ## Optimalisation
# es_vormstrategie = cma.CMAEvolutionStrategy(vormstrategie.initialvalue(), 1000)
# logger_vormstrategie = cma.CMADataLogger('outputvormstrategie').register(es_vormstrategie)
#  
#  
#     
# ## Draw in in difrent filles
# if printpreviousresult_vormstrategie:
#     result_vormstrategie = printpreviousresult_vormstrategie
# else:
#     es_vormstrategie.optimize(vormstrategie.fitness, logger=logger_vormstrategie)
#     es_vormstrategie.result_pretty()
# 
#     result_vormstrategie = es_vormstrategie.result()[0]
# 
# print('Result: [' + ', '.join(map(str,result_vormstrategie)) + ']')
# print('Fitness: ' + str(vormstrategie.fitness(result_vormstrategie)))
     
     
steps = logger.load().data()["xrecent"]
i = 0
while i < len(steps):
    print("%d of %d" % (i + 1, len(steps)))
    print(steps[i][5:])
    draw(airport, steps[i][5:], numrunways, i)
         
    i += 1
#  
#means = logger.load().data()["xmean"]
print('Result: [' + ', '.join(map(str,result)) + ']')
print('Fitness: ' + str(min([step[4] for step in steps])))
 
##Drawpolt
draw_plots(fitnessnumbers=[step[4] for step in steps])#, [fitness(mean[5:]) for mean in means])

draw(airport, result, numrunways)
 
# steps_vormstrategie = logger_vormstrategie.load().data()["xrecent"]
# 
# i = 0
# while i < len(steps_vormstrategie):
#     print("%d of %d" % (i + 1, len(steps_vormstrategie)))
#     print(steps_vormstrategie[i][5:])
#     draw(airport, result, numrunways, steps_vormstrategie[i][5:], vormstrategie.construct, i)
#      
#     i += 1
# 
# 
# #means_vormstrategie = logger_vormstrategie.load().data()["xmean"]
# 
# print('Result: [' + ', '.join(map(str,result_vormstrategie)) + ']')
# print('Fitness: ' + str(vormstrategie.fitness(result_vormstrategie)))
# 
# ##Drawpolt
# draw_plots([step_vormstrategie[4] for step_vormstrategie in steps_vormstrategie])#, [vormstrategie.fitness(mean_vormstrategie[5:]) for mean_vormstrategie in means_vormstrategie])
# 
# 
# draw(airport, result, numrunways,result_vormstrategie, vormstrategie.construct)

