import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
from draw_runways_gatefield import draw
from draw_plots import draw_plots
from shape_strategy.gate_fitness import buffergate
import shape_strategy.line_segments as shapestrategy


# #airport Zaventem
# airport = geometry.Polygon([(-3887.5338, -15111.0947), (-4667.0044, -15075.6949), (-5206.3351, -14823.9632), (-5351.9938, -14894.7628), (-5690.5518, -14894.7628), (-5812.5901, -14407.0326), (-3667.0351, -13434.6257), (-3493.8194, -13517.2251), (-1625.8886, -12201.2692), (-1134.4820, -12251.2332), (-847.9250, -12831.8033), (-847.9250, -13066.4173), (-903.6444, -13352.7258), (-748.1866, -13807.8867), (-1026.7836, -14002.7356), (-891.1957, -14196.6008), (-645.5707, -14024.8123), (-478.4202, -14263.8059), (-445.6536, -14794.6836), (-374.8073, -14762.2405), (-224.9005, -14519.1844), ( 322.1703, -14333.9870), ( 489.5638, -14333.9870), ( 764.9966, -14504.7204), ( 793.5264, -14594.9865), ( 772.9215, -14680.5018), ( 642.9524, -14739.0956), ( -56.8857, -14999.0798), (-329.0749, -15184.6179), (-428.2840, -15156.6601), (-512.2302, -15156.6601), (-558.0190, -15197.3260), (-608.9783, -15356.6108), (-717.7563, -15533.3608), (-888.8519, -15668.8285), (-1350.3456, -15856.8472), (-1439.2633, -15856.8472), (-1595.8319, -15830.0995), (-1643.0105, -15829.5983), (-1702.7810, -15850.8541), (-1756.4732, -15888.3048), (-1796.9956, -15977.3768), (-1938.2913, -16236.8780), (-2038.4792, -16403.9284), (-2132.0601, -16533.5514), (-2228.8904, -16486.1521), (-2270.4820, -16375.1211), (-2286.0788, -16297.2046), (-2375.5261, -16174.4249), (-2451.9431, -16094.9365), (-2503.2366, -16062.5136), (-2582.7940, -16042.6415), (-2885.8776, -16053.6926), (-3126.3924, -16045.1804), (-3232.6228, -16006.4314), (-3402.9289, -15802.5783), (-3429.9081, -15590.3015), (-3402.9620, -15480.0297), (-3345.6312, -15390.7386), (-3428.3508, -15015.4501), (-3887.5338, -15111.0947)])
# ## gatebuilding,  ratio between length and width
# minairportfield = 2015472
# ratiolb= 1.5
# ## terminalbuilding
# agate_min = 185842
# agate_max = (agate_min + (agate_min * 0.1))
# pgate_min = 4890
# pgate_max =pgate_min + (pgate_min * 0.1)
# ## runways
# numrunways = 2
# preferredangledegrees = [25,25]


# ##airport Heathrow
airport = geometry.Polygon([(-4383.0617, 5622.0932), (-4457.2097, 5677.6747), (-4841.6601, 5677.6747), (-4906.3434, 5661.8623), (-5049.1226, 5659.6646), (-5087.2358, 5659.6646), (-5129.2159, 5673.4331), (-5181.1143, 5700.1146), (-5229.5197, 5735.6352), (-5264.0719, 5784.4920), (-5279.1375, 5813.7731), (-5308.9950, 5840.5916), (-5333.3732, 5854.0005), (-5349.0671, 5861.4544), (-5429.1295, 5869.4808), (-5457.1120, 5876.1401), (-5500.6231, 5897.0386), (-5521.8206, 5917.3803), (-5541.0659, 5946.3600), (-5548.3291, 5973.3031), (-5553.0714, 5997.8246), (-5553.0714, 6025.9682), (-5546.3770, 6060.5210), (-5500.3959, 6208.6594), (-5485.1495, 6301.0857), (-5479.3203, 6406.4605), (-5479.3203, 6482.4742), (-5477.1971, 6583.9700), (-5477.1971, 6649.0327), (-5482.3840, 6687.2593), (-5499.9921, 6740.0346), (-5523.6332, 6808.7856), (-5545.6380, 6860.0813), (-5583.6877, 6923.2846), (-5688.0410, 7050.9379), (-5725.3731, 7133.4131), (-5755.9570, 7211.7577), (-5765.6719, 7255.6627), (-5772.1476, 7318.9781), (-5772.1476, 7394.9635), (-5705.4288, 7623.1416), (-5681.8350, 7657.3908), (-5641.9673, 7683.1629), (-5557.5328, 7709.5184), (-5347.9177, 7749.9896), (-5206.2747, 7776.2076), (-5079.8385, 7784.7552), (-4853.4365, 7785.6287), (-4640.8975, 7871.8261), (-4440.1991, 7870.8853), (-4429.5779, 7860.5403), (-4429.5779, 7834.5098), (-4386.8391, 7827.0187), (-4386.8391, 7800.6137), (-4380.2788, 7774.5829), (-4077.0192, 7773.0228), (-3496.8556, 7773.2536), (-2570.2031, 7776.3472), (-2432.0782, 7806.1410), (-1444.5414, 7808.2087), (-929.2628, 7796.6956), (-709.1047, 7796.3896), (-653.0671, 7792.9175), (-610.8655, 7759.9222), (-602.1101, 7737.0192), (-599.1535, 7613.2096), (-575.8454, 7452.3525), (-523.6671, 7423.4812), (-245.7443, 7412.1378), (-134.9650, 7406.5238), ( -45.8603, 7373.6428), (  20.7680, 7322.3163), (  46.6448, 7261.0604), ( 101.1497, 7160.1002), ( 171.1450, 7066.7905), ( 291.0496, 6915.3993), ( 385.4339, 6703.3415), ( 410.9867, 6646.0507), ( 404.1617, 6616.6761), ( 240.8829, 6520.3401), (  -0.7148, 6398.5986), (-565.9514, 6067.2155), (-994.7759, 5772.4123), (-1279.3698, 5579.6760), (-1470.6108, 5462.6019), (-1597.5312, 5462.6019), (-1677.5168, 5452.0528), (-1765.6504, 5375.4505), (-1848.3496, 5265.6768), (-1886.0065, 5213.0677), (-1968.2903, 5171.7000), (-2108.3673, 5104.9474), (-2280.4250, 5004.9707), (-2371.7546, 4982.6256), (-2456.3727, 4976.9435), (-2503.8565, 4976.9435), (-2555.3094, 4992.3572), (-2626.2821, 5050.7804), (-2673.5733, 5078.4038), (-2725.6778, 5079.8594), (-2773.0851, 5068.9791), (-2828.1795, 5078.5793), (-2870.4620, 5097.1403), (-2959.5100, 5127.2210), (-3054.1391, 5147.3654), (-3252.8506, 5179.5576), (-3387.6361, 5193.7342), (-3497.3344, 5213.8008), (-3743.6436, 5255.5205), (-3823.9615, 5264.1622), (-4033.6945, 5291.7450), (-4116.9778, 5325.3689), (-4157.9426, 5353.8925), (-4216.9630, 5414.1299), (-4274.0654, 5484.8192), (-4336.5180, 5582.0526), (-4355.6090, 5600.3735), (-4383.0617, 5622.0932)])
## gatebuilding,  ratio between length and width
minairportfield = 4872684
ratiolb= 8.5
## terminalbuilding
agate_min = 472684
agate_max = (agate_min + (agate_min * 0.1))
pgate_min =18774
pgate_max =pgate_min + (pgate_min * 0.1)
## runways
numrunways = 2
preferredangledegrees = [0,0]

# #airport Schiphol
# airport = geometry.Polygon([(-50077.7028, 1521.1805), (-50243.1582, 1007.8382), (-50495.5842,  511.0635), (-50771.6035,  136.8051), (-50541.7521, -225.1390), (-51430.1220, -789.2953), (-51171.6535, -1061.6272), (-51111.4998, -1023.4318), (-51088.3089, -1059.9548), (-48456.0788,  611.4166), (-48389.1996,  516.0507), (-47886.5930,  868.5236), (-48012.9185, -1070.9342), (-47975.8699, -1105.4832), (-47790.6258, -1130.1613), (-47555.6333, -1126.0536), (-47410.6152, -953.9200), (-47170.9609, -764.9339), (-46893.7288, -458.3998), (-46564.4315,  -20.7477), (-46435.2533,  514.5938), (-46370.3985,  708.9892), (-46226.5368,  871.4725), (-46078.2992, 1005.6978), (-45893.0009, 1152.2656), (-45749.3946, 1249.4633), (-45654.2732, 1299.4249), (-45443.0138, 1407.8420), (-45238.4758, 1533.5292), (-45147.9004, 1628.7027), (-44961.3073, 1900.2977), (-44832.7722, 2148.0394), (-44818.7581, 2299.9783), (-46129.5016, 3350.2107), (-46206.1932, 3398.2895), (-46269.5028, 3410.6670), (-46639.6719, 3380.4638), (-46714.8593, 3454.0844), (-46752.4842, 3476.4249), (-46941.9265, 3409.0105), (-47364.8936, 3762.5142), (-47467.1488, 3834.6321), (-47551.3590, 3852.6615), (-47623.5387, 3851.1592), (-47680.6821, 3830.1248), (-47761.8847, 3755.0018), (-47803.9899, 3646.8244), (-47880.6815, 3552.1698), (-47988.0373, 3377.1200), (-48100.8188, 3249.4109), (-48157.9612, 3196.8247), (-48209.5815, 3187.2684), (-50040.2755, 3104.0903), (-49973.5918, 4363.0546), (-50243.1554, 4602.2022), (-50215.5099, 5172.2799), (-50571.0544, 5474.1168), (-50754.6362, 5481.0823), (-51155.3770, 3661.6532), (-51751.4923, 4339.2185), (-52626.9427, 5089.6384), (-52531.1904, 6635.6057), (-52654.2420, 6739.4261), (-52607.7204, 7687.0238), (-52561.2338, 7741.6662), (-52520.1370, 8850.0655), (-52536.2377, 8883.9236), (-52648.3993, 8980.5425), (-52883.5171, 8998.5207), (-52920.0641, 8963.2118), (-53184.0615, 4064.9286), (-53093.1197, 4033.4044), (-53061.5674, 3987.0452), (-52952.0664, 3977.7733), (-52920.5141, 4022.2784), (-52862.9796, 4022.2784), (-52811.0131, 4053.8026), (-52814.7242, 4281.8898), (-52721.9263, 4374.6080), (-52606.8562, 4307.8510), (-52469.5149, 4480.3071), (-51172.5549, 3350.5150), (-51318.8366,  700.9687), (-51266.3319,  596.0509), (-51090.4432,  546.2148), (-50822.6722,  588.1820), (-50547.0254,  748.1817), (-50339.6341, 1222.9352), (-50260.8367, 1475.9186), (-50345.3020, 1649.0750), (-50272.0029, 1864.4753), (-50132.2015, 1816.9019), (-49909.0593, 2472.6389), (-49741.1503, 2465.1106), (-49972.7680, 1905.8934), (-49607.2476, 1810.5330), (-49580.1051, 1686.8031), (-49692.2943, 1477.9030)])
# # gatebuilding,   ratio between length and width
# minairportfield = 3162667
# ratiolb= 1.9
# # terminalbuilding
# agate_min = 306611
# agate_max = (agate_min + (agate_min * 0.1))
# pgate_min = 10026
# pgate_max =pgate_min + (pgate_min * 0.1)
# # runways
# numrunways = 2
# preferredangledegrees = [87,87]


# ##airport Beijing internationa airport
# airport = geometry.Polygon([(-48628.2250, -17699.1477), (-49213.7585, -17755.5587), (-49541.7998, -17787.1627), (-49848.0964, -15313.1147), (-51345.0596, -15495.9004), (-51791.0742, -11843.1662), (-51694.7516, -11831.4048), (-51742.9011, -11474.8481), (-51584.9302, -11467.2324), (-51524.5534, -11924.8549), (-51441.2196, -11914.4748), (-51418.7527, -12094.8442), (-48134.1846, -11660.1059), (-47644.0425, -13436.4039), (-47179.8782, -17536.8711), (-47298.0248, -17547.2504), (-47253.3625, -18055.6390), (-47456.7920, -18073.5104), (-47502.5921, -17590.7028), (-47729.5095, -17612.5643), (-47665.8742, -18319.3125), (-48555.7641, -18405.0457)])
# ## gatebuilding,   ratio between length and width
# minairportfield = 4506770
# ratiolb= 5.5
# ## terminalbuilding
# agate_min = 646725
# agate_max = (agate_min + (agate_min * 0.1))
# pgate_min = 14213
# pgate_max =pgate_min + (pgate_min * 0.1)
# ## runways
# numrunways = 2
# preferredangledegrees = [97,97]


## runways
minrunwaylength = 3500
minrunwaywidth = 60
# numrunways = 2
# preferredangledegrees = [25,25]
usedtogether = [[1],[0]]
preferredangle = []
for i in range(0, numrunways):
    preferredangle.append(1.0 * (preferredangledegrees[i] % 180) / 360 * 2*math.pi)

## buffer between runway and gatefield
bufferbetweenrg = 125

printpreviousresult = [-3017.64557438, 6074.80198353, 4474.23512662, 6789.53384295, 6283.18530718, -3054.46001097, 7614.53116189, 4513.80945821, 6775.83881863, -9424.77796077, -3032.29317555, 6847.16645445, 11434.2407175, 44470.2960082, -1574.22708058]
printpreviousresult_shapestrategy = None

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
            errors += 1000000*(1-length)
        if width <= 0.1:
            errors += 1000000*(1-width)
        
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
                areaoutsideairport = polygon.difference(airport).area / polygon.area * 100 # Percent of terminal that's outside airport
            except:
                print "Error: (%d %d) (%d %d) (%d %d) (%d %d) %d %d" % (x1, y1, x2, y2, x3, y3, x4, y4, length, width)
            res += 1 * (10 + areaoutsideairport)
             
            if areaoutsideairport > 99:
                # Try to guide terminal towards airport
                res += 1 *airport.centroid.distance(polygon.centroid)
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
                res += 1000*angledifference 
                
                #print('D=', res)
                
            else:
                res += 1000*(math.pi - angledifference) 
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
es = cma.CMAEvolutionStrategy(numrunways * [airport.centroid.coords[0][0], airport.centroid.coords[0][1], minrunwaylength, minrunwaywidth*100, 0] + [airport.centroid.coords[0][0], airport.centroid.coords[0][1], 1000*10, 1000*10,0], 1000)
 
logger = cma.CMADataLogger().register(es)
     
## Draw in in difrent filles
if printpreviousresult:
    result = printpreviousresult
else:
    es.optimize(fitness, logger=logger)
    es.result_pretty()
    result = es.result()[0]
 
print('Result: [' + ', '.join(map(str,result)) + ']')
  
##uit result haal je plaats voor gate. 
coords= result[numrunways*5:]
  
x = coords[0]
y = coords[1]
length = coords[2]/10
width = coords[3]/10
angle = coords[4]/1000
  
x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
   
x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
   
x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
   
x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
   
gatebuilding_polygon = geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])
 
## runwaypoints
x1 = result[0] + result[2] * math.cos(result[4]) / 2
y1 = result[1] + result[2] * math.sin(result[4]) / 2
  
x2 = result[0] - result[2] * math.cos(result[4]) / 2
y2 = result[1] - result[2] * math.sin(result[4]) / 2
 
x3 = result[5] + result[7]  * math.cos(result[9]) / 2
y3 = result[6] + result[7]  * math.sin(result[9]) / 2
  
x4 = result[5] - result[7]  * math.cos(result[9]) / 2
y4 = result[6] - result[7]  * math.sin(result[9]) / 2
         
runwaypoints = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
  
shapestrategy.setairport(gatebuilding_polygon)
shapestrategy.setmeasures(agate_min, agate_max, pgate_min, pgate_max)#, runwaypoints)
 
 
## Optimalisation
es_shapestrategy = cma.CMAEvolutionStrategy(shapestrategy.initialvalue(), 1000)
logger_shapestrategy = cma.CMADataLogger('outputshapestrategy').register(es_shapestrategy)
    
    
## Draw in in difrent filles
if printpreviousresult_shapestrategy:
    result_shapestrategy = printpreviousresult_shapestrategy
else:
    es_shapestrategy.optimize(shapestrategy.fitness, logger=logger_shapestrategy)
    es_shapestrategy.result_pretty()
   
    result_shapestrategy = es_shapestrategy.result()[0]
   
print('Result: [' + ', '.join(map(str,result_shapestrategy)) + ']')
      
      
steps = logger.load().data()["xrecent"]
#i = 0
#while i < len(steps):
#    print("%d of %d" % (i + 1, len(steps)))
#    print(steps[i][5:])
#    draw(airport, steps[i][5:], numrunways, filenamenum=i, ofnum=len(steps))
#           
#    i += 1
   
means = logger.load().data()["xmean"]
print('Result: [' + ', '.join(map(str,result)) + ']')
print('Fitness: ' + str(min([step[4] for step in steps])))
print('Result landingsbanen:         [' + ', '.join(map(str,result)) + ']')
print('Fitness landingsbanen:        ' + str(min([step[4] for step in steps])))
print('Afmeting landingsbaan 1:      ' + str(result[2]) + ' x ' + str(result[3]/100))
print('Afmeting landingsbaan 2:      ' + str(result[7]) + ' x ' + str(result[8]/100))
print('Oppervlakte platform:         ' + str(result[12] * result[13]/100))

  
#Drawpolt
draw_plots(fitnessnumbers=[step[4] for step in steps])#, [fitness(mean[5:]) for mean in means])
draw(airport, result, numrunways, ofnum=len(steps))
  
steps_shapestrategy = logger_shapestrategy.load().data()["xrecent"]
means_shapestrategy = logger_shapestrategy.load().data()["xmean"]
    
i = 0
while i < len(steps_shapestrategy):
    print("%d of %d" % (i + 1, len(steps_shapestrategy)))
    print(steps_shapestrategy[i][5:])
    draw(airport, result, numrunways, steps_shapestrategy[i][5:], means_shapestrategy[i][5:], shapestrategy.construct, i, len(steps_shapestrategy))
              
    i += 1
      
#means_shapestrategy = logger_shapestrategy.load().data()["xmean"]
  
  
  
## print info shape_strategy
gatespolygon = shapestrategy.construct(result_shapestrategy)
  
## check if its a list, make a list
if isinstance(gatespolygon, list):
    gatebuildings = gatespolygon
else:
    try:
        gatebuildings = gatespolygon.geoms
    except AttributeError:
        gatebuildings = [gatespolygon]
  
totalarea = 0
totalperiphery = 0
try:
    allgates = gatebuildings[0]
    for polygon in gatebuildings[1:]:
        allgates = allgates.union(polygon)
    totalarea = allgates.area
    allgates = allgates.buffer(buffergate)
    totalperiphery = allgates.boundary.length
except:
    pass
  
print('Result vormstrategie:         [' + ', '.join(map(str,result_shapestrategy)) + ']')
print('Fitness vormstrategie:        ' + str(min([step_shapestrategy[4] for step_shapestrategy in steps_shapestrategy])))
print('Gegeven oppervlakte:          ' + str(agate_min) + ' - ' + str(agate_max))
print('Geoptimaliseerde oppervlakte: ' + str(totalarea))
print('Gegeven omtrek:               ' + str(pgate_min) + ' - ' + str(pgate_max))
print('Geoptimaliseerde omtrek:      ' + str(totalperiphery))
print('Aantal vliegtuigen:           ' + str(int(totalperiphery / 45)))
shapestrategy.printline(result_shapestrategy)
 
#Drawpolt
draw_plots([step_shapestrategy[4] for step_shapestrategy in steps_shapestrategy])#, [shape_strategy.fitness(mean_shapestrategy[5:]) for mean_shapestrategy in means_shapestrategy])
   
   
draw(airport, result, numrunways,result_shapestrategy, None, shapestrategy.construct, ofnum=len(steps_shapestrategy))
draw(airport, result, numrunways,result_shapestrategy, None, shapestrategy.construct, ofnum=len(steps_shapestrategy), merge=True)
  

