import shapely.affinity as affinity
import shapely.geometry as geometry
import cma
import math
import graphics
from optimise import optimise

##airport zaventem
airport = geometry.Polygon([(-4175.9299,  543.2448), (-4955.4006,  578.6446), (-5494.7312,  830.3763), (-5640.3899,  759.5767), (-5978.9479,  759.5767), (-6100.9862, 1247.3069), (-3955.4312, 2219.7139), (-3782.2155, 2137.1144), (-2143.2504, 3291.7641), (-1914.2847, 3453.0703), (-1422.8781, 3403.1063), (-1136.3211, 2822.5362), (-1136.3211, 2587.9222), (-1192.0405, 2301.6137), (-1036.5827, 1846.4528), (-1315.1798, 1651.6039), (-1179.5918, 1457.7388), (-933.9668, 1629.5272), (-766.8164, 1390.5336), (-734.0497,  859.6560), (-663.2034,  892.0990), (-579.4244, 1027.9368), (-513.2966, 1135.1551), (-164.9863, 1253.0670), (  33.7742, 1320.3525), ( 201.1677, 1320.3525), ( 476.6005, 1149.6191), ( 505.1303, 1059.3530), ( 484.5254,  973.8377), ( 354.5562,  915.2439), (-345.2818,  655.2597), (-617.4710,  469.7216), (-716.6801,  497.6794), (-800.6263,  497.6794), (-846.4152,  457.0135), (-897.3744,  297.7288), (-1006.1524,  120.9787), (-1177.2480,  -14.4890), (-1509.7546, -149.9567), (-1638.7417, -202.5077), (-1727.6594, -202.5077), (-1884.2280, -175.7600), (-1931.4066, -175.2588), (-1991.1771, -196.5146), (-2044.8693, -233.9653), (-2085.3917, -323.0373), (-2226.6874, -582.5385), (-2326.8753, -749.5889), (-2420.4562, -879.2118), (-2517.2865, -831.8126), (-2558.8781, -720.7816), (-2574.4749, -642.8651), (-2663.9222, -520.0854), (-2740.3392, -440.5970), (-2791.6327, -408.1741), (-2871.1901, -388.3020), (-3174.2737, -399.3531), (-3414.7885, -390.8409), (-3521.0189, -352.0919), (-3691.3250, -148.2388), (-3718.3042,   64.0380), (-3691.3581,  174.3099), (-3634.0273,  263.6009), (-3716.7469,  638.8895), (-4175.9299,  543.2448)])
areaterminalbuilding = 250000

printpreviousresult = None

minrunwaylength = 3500
minrunwaywidth = 40
numrunways = 2
#numrunways = 0


preferredangledegrees = [60,60]
usedtogether = [[1],[0]]
preferredangle = []
for i in range(0, numrunways):
	preferredangle.append(1.0 * (preferredangledegrees[i] % 180) / 360 * 2*math.pi)

#maxarea = 150000

def fitness(coords):
	res = 0
	errors = 0

##runways
	runwaypolygons = []
	for i in range(0,numrunways):
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		length = coords[i*5 + 2]
		width = coords[i*5 + 3]/100
		angle = coords[i*5 + 4]/1000
 		
		if length <= 0.1:
			errors += 1000*(1-length)
		if width <= 0.1:
			errors += 1000*(1-width)
		
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
 		
		polygon = geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])
 		
		runwaypolygons.append(polygon)
 		
		if not airport.contains(polygon):
			try:
				areaoutsideairport = 10 + polygon.difference(airport).area / polygon.area * 100 # Percent of terminal that's outside airport
			except:
				print "Error: (%d %d) (%d %d) (%d %d) (%d %d) %d %d" % (x1, y1, x2, y2, x3, y3, x4, y4, length, width)
			res += areaoutsideairport
 			
			if areaoutsideairport > 99:
				# Try to guide terminal towards airport
				res += airport.centroid.distance(polygon.centroid)
 			
		if length < minrunwaylength:
			res += (10 + minrunwaylength-length)
			
		if width < minrunwaywidth:
			res += (10 + minrunwaywidth-width)
		angledifference = (preferredangle[i] - angle) % math.pi
		
		if angledifference < math.pi / 2:
			res += angledifference
		else:
			res += math.pi - angledifference
 		
 	if not errors:
		for i in range(0, numrunways):
			for j in usedtogether[i]:
				if runwaypolygons[i].intersects(runwaypolygons[j]):
					res += (10 + runwaypolygons[i].intersection(runwaypolygons[j]).area)			
	
	if errors:
		return errors
	
##gatebuilding	
	gatespolygon = constructlsystem(coords[numrunways*5:])
	
	## if constructlsystem didn't produce annything -> return 1000000
	if gatespolygon:
		res += gatefitness(airport, gatespolygon)
	else:
		return res + 1000000

	try:
		for i in range(0,numrunways):
			if runwaypolygons[i].intersects(gatespolygon):
				res += (10 + runwaypolygons[i].intersection(gatespolygon).area)
	except:
		return res + 1000000
	
	return res

def constructlsystem(coords):
	## Dragon curve
	#axiom = "F"
	#rules = dict([("F", "FF+[+F-F-F]-[-F+F+F]")])
	#theta = math.pi/2
	
	## Pythogoras tree
# 	axiom = "0"
# 	rules = dict([("1", "11"), ("0", "1[-0]+0")])
# 	theta = math.pi/4
	
	## random construction
	axiom = "F"
	alphabet = ["", "F", "G", "+", "-", "[", "]"]
	maxletters = 5
	theta = math.pi/4

	rules = []
	rule = ""
	
	for c in range(0, maxletters):
		rulenumber = int(coords[2 + c])
		rule += alphabet[rulenumber % 7]

	rules.append(("F", rule))
	rules = dict(rules)
	print(rules)
	
	current = axiom
	
	polygon = None
	i = 0
	while True:
		[x, y] = coords[:2]
		l = 300
		w = 60
		
		angle = 0
		positions = []
		polygons = []
		
		print(current)
		for char in current:
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
		
		prevpolygon = polygon
		if len(polygons):
			polygon = polygons[0]
			for p in polygons[1:]:
				try:
					polygon = polygon.union(p)
				except:
					return None
		else:
			polygon = None
		
		#if polygon.area > maxarea:
		#	return prevpolygon
		
		if i >= 4:
			if polygon:
				scalefactor = math.sqrt(polygon.area / areaterminalbuilding)
				polygon = affinity.scale(polygon, xfact=1.0/scalefactor, yfact=1.0/scalefactor, zfact=1.0, origin='center')
			return polygon
		
		new = ""
		
		for char in current:
			new += rules.get(char, char)
		
		current = new
		i += 1
		

def gatefitness(airport, gatespolygon):
	res = 0
	
	if not gatespolygon:
		return 100000
	
	try:
		gatebuildings = gatespolygon.geoms
	except AttributeError:
		gatebuildings = [gatespolygon]
		
	try:
		for gatebuilding in gatebuildings:
			if not airport.contains(gatebuilding):
				areaoutsideairport = 10 + gatebuilding.difference(airport).area / gatebuilding.area * 100 # Percent of terminal that's outside airport
				res += areaoutsideairport
				
				if areaoutsideairport > 99:
					# Try to guide terminal towards airport
					res += airport.centroid.distance(gatebuilding.centroid)
			else:
				res += gatebuilding.area - gatebuilding.exterior.length
	except:
		return 100000
		
	return res

## Optimalisation
es = cma.CMAEvolutionStrategy(numrunways * [airport.centroid.coords[0][0], airport.centroid.coords[0][1], minrunwaylength, minrunwaywidth*100, 0] + [airport.centroid.coords[0][0], airport.centroid.coords[0][1], 0, 0, 0, 0, 0], 1000)
optimise(airport,numrunways, fitness, constructlsystem, es, printpreviousresult)

# win = graphics.GraphWin('L-systeem', 600, 600) # give title and dimensions
# win.setCoords(-5000, 0, 0, 5000)
#     
#     
#res = [2758.89514702, 3021.78000072, 4406.09900556, 1861.65501302, -1238.43759662, -7803.213031, -633.008330616, 6152.88319123, 10.0, -5764.22537014, -1310.10483508, 7492.53691164, 199.807136089, -2814.49594531, 3341.51444447, -2311.27341127, -4050.24911266]
#print(fitness(res))
# lsystem = constructlsystem(res[numrunways*5:])
#     
# try:
# 	gatebuildings = lsystem.geoms
# except AttributeError:
# 	gatebuildings = [lsystem]
#     
# for gatebuilding in gatebuildings:
# 	gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), gatebuilding.exterior.coords))
# 	gatebuildinggraphic.py(win)
#     	
# 	for interior in gatebuilding.interiors:
# 		gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), interior.coords))
# 		gatebuildinggraphic.py(win)
#     
# win.getMouse()
# win.close()