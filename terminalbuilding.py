import graphics
import shapely.geometry as geometry
import cma, math

#airport = geometry.Polygon([(0,0), (500, 1000), (2500, 1000), (1500, 3000), (0, 3000)])
airport = geometry.Polygon([(-4175.9299,  543.2448), (-4955.4006,  578.6446), (-5494.7312,  830.3763), (-5640.3899,  759.5767), (-5978.9479,  759.5767), (-6100.9862, 1247.3069), (-3955.4312, 2219.7139), (-3782.2155, 2137.1144), (-2143.2504, 3291.7641), (-1914.2847, 3453.0703), (-1422.8781, 3403.1063), (-1136.3211, 2822.5362), (-1136.3211, 2587.9222), (-1192.0405, 2301.6137), (-1036.5827, 1846.4528), (-1315.1798, 1651.6039), (-1179.5918, 1457.7388), (-933.9668, 1629.5272), (-766.8164, 1390.5336), (-734.0497,  859.6560), (-663.2034,  892.0990), (-579.4244, 1027.9368), (-513.2966, 1135.1551), (-164.9863, 1253.0670), (  33.7742, 1320.3525), ( 201.1677, 1320.3525), ( 476.6005, 1149.6191), ( 505.1303, 1059.3530), ( 484.5254,  973.8377), ( 354.5562,  915.2439), (-345.2818,  655.2597), (-617.4710,  469.7216), (-716.6801,  497.6794), (-800.6263,  497.6794), (-846.4152,  457.0135), (-897.3744,  297.7288), (-1006.1524,  120.9787), (-1177.2480,  -14.4890), (-1509.7546, -149.9567), (-1638.7417, -202.5077), (-1727.6594, -202.5077), (-1884.2280, -175.7600), (-1931.4066, -175.2588), (-1991.1771, -196.5146), (-2044.8693, -233.9653), (-2085.3917, -323.0373), (-2226.6874, -582.5385), (-2326.8753, -749.5889), (-2420.4562, -879.2118), (-2517.2865, -831.8126), (-2558.8781, -720.7816), (-2574.4749, -642.8651), (-2663.9222, -520.0854), (-2740.3392, -440.5970), (-2791.6327, -408.1741), (-2871.1901, -388.3020), (-3174.2737, -399.3531), (-3414.7885, -390.8409), (-3521.0189, -352.0919), (-3691.3250, -148.2388), (-3718.3042,   64.0380), (-3691.3581,  174.3099), (-3634.0273,  263.6009), (-3716.7469,  638.8895), (-4175.9299,  543.2448)])

#terminallenghtx= 300
#terminalwidthy= 90
#beginpointx = 1000
#beginpointy = 1000

#terminalbuilding = geometry.Polygon([(beginpointx,beginpointy),(beginpointx+terminallenghtx,beginpointy),(beginpointx+terminallenghtx,beginpointy+terminalwidthy),(beginpointx,beginpointy+terminalwidthy) ])
terminalbuilding = geometry.Polygon([(-3002.2269, 782.2334),( -2868.7354, 834.4152),( -2982.1092, 1085.2988),( -3102.3257, 1038.3062)])
	
mingatelength = 600
mingatewidth = 60
minrunwaylength = 2700
minrunwaywidth = 40



numgate = 3
numrunways = 2
preferredangledegrees = [60,60]
usedtogether = [[1],[0]]

preferredangle = []
for i in range(0, numrunways):
	preferredangle.append(1.0 * (preferredangledegrees[i] % 180) / 360 * 2*math.pi)


def fitness(coords):
	res = 0
	gatepolygons = []
	runwaypolygons = []
	
	for i in range(0, numgate + numrunways):
		if i < numrunways:
			isrunway = True
			isgate = False
		else:
			isrunway = False
			isgate = True

		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		length = coords[i*5 + 2]
		width = coords[i*5 + 3]/100
		angle = coords[i*5 + 4]/1000
			
		if isgate:
			length = mingatelength
			width = mingatewidth
		
		if length <= 0.1:
			return 1000*(1-length)
		
		if width <= 0.1:
			return 1000*(1-width)	

		x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		polygon = geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])
		
		if isgate:
			gatepolygons.append(polygon)
			
		if isrunway:
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
		
		if isgate:	
			if length < mingatelength:
				res += (10 + mingatelength - length)
			if length > mingatelength:	
				res += (10 - mingatelength + length)
			
			if width < mingatewidth:
				res += (10 + mingatewidth - width)
				if width > mingatewidth:
					res += (10 - mingatewidth + width)
					
		if isrunway:		
			if length < minrunwaylength:
				res += (10 + minrunwaylength-length)
			
			if width < minrunwaywidth:
				res += (10 + minrunwaywidth-width)
			angledifference = (preferredangle[i] - angle) % math.pi
		
			if angledifference < math.pi / 2:
				res += angledifference
			else:
				res += math.pi - angledifference

	for i in range(0, numrunways):
		for j in usedtogether[i]:
			if runwaypolygons[i].intersects(runwaypolygons[j]):
				res += (10 + runwaypolygons[i].intersection(runwaypolygons[j]).area)
					
	for i in range(0,numrunways):
		for j in range (0, numgate):
			if runwaypolygons[i].intersects(gatepolygons[j]):
				res += (10 + runwaypolygons[i].intersection(gatepolygons[j]).area)

	allgates = gatepolygons[0]
	for polygon in gatepolygons[1:]:
		allgates = allgates.union(polygon)
	allgates = allgates.buffer(130)
	gateperiphery = allgates.union(terminalbuilding).intersection(airport).boundary.difference(terminalbuilding.boundary).difference(airport.boundary)

	res -= gateperiphery.length / 5
	
	##Kruskal's algorithm
	distances = []
	comp = {}
	totaldistance = 0
	
	#iteration over all the building
	for i in range(-1, len(gatepolygons)):
		if i >= 0:
			building1 = gatepolygons[i]
		else:
			building1 = terminalbuilding
		comp[i] = {i}
		
		#iteration in an iteration to find the distance between 2 buildings	
		for j in range(i+1, len(gatepolygons)):
			building2 = gatepolygons[j]
			# make a list with distance between 2 buildings and building A an B, and later sort them on smallest distance
			distances.append((building1.distance(building2), i, j ))
	distances.sort()

	#iterate n - 1 times, with n = number of buildings
	for p in range(1, len(gatepolygons)+1):
		# the fist time, the lowest distance is the 1ste number because of the sort list
		lowest= distances.pop(0)
		a = lowest[1]
		b = lowest[2]
		
		# if this edge creates a loop take the next lowest distance instead
		while b in comp[a]:
			lowest = distances.pop(0)
			a = lowest[1]
			b = lowest[2]
		totaldistance = totaldistance + lowest[0]
		# For each node, update the set of nodes with are in the same componetns 
		for v in comp[a]:
			comp[v] = comp[v].union(comp[b])
		for v in comp[b]:
			comp[v] = comp[v].union(comp[a])

	res += totaldistance
	
	return res
	
def draw(coords):
	win = graphics.GraphWin('airport', 600, 600*(airport.bounds[3] - airport.bounds[1])/(airport.bounds[2] - airport.bounds[0])) # give title and dimensions
	win.setCoords(airport.bounds[0] - 10, airport.bounds[1] - 10, airport.bounds[2] + 10, airport.bounds[3] + 10)

	airportgraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), airport.exterior.coords))
	airportgraphic.draw(win)
	
	terminalbuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), terminalbuilding.exterior.coords))
	terminalbuildinggraphic.setOutline("cyan")
	terminalbuildinggraphic.draw(win)

	colours = {
		0: "red",
		1: "blue",
		2: "green",
		3: "yellow",
		4: "magenta",
		5: "cyan",

	}
	
	#for i in range(0, numgate):
		#colours[i] = "black"
	
	for i in range(0, numgate + numrunways):
		if i < numrunways:
			isrunway = True
			isgate = False
		else:
			isrunway = False
			isgate = True
	
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		length = coords[i*5 + 2]
		width = coords[i*5 + 3]/100
		angle = coords[i*5 + 4]/1000
		colour = colours.get(i, "black")
		
		if isrunway:
			colour = "black"
		
		if isgate:
			length = mingatelength
			width = mingatewidth
			
		x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
	
		runway1 = graphics.Line(graphics.Point(x1, y1), graphics.Point(x2, y2))
		runway1.setOutline(colour)
		runway1.draw(win)
		runway2 = graphics.Line(graphics.Point(x2, y2), graphics.Point(x3, y3))
		runway2.setOutline(colour)
		runway2.draw(win)
		runway3 = graphics.Line(graphics.Point(x3, y3), graphics.Point(x4, y4))
		runway3.setOutline(colour)
		runway3.draw(win)
		runway4 = graphics.Line(graphics.Point(x4, y4), graphics.Point(x1, y1))
		runway4.setOutline(colour)
		runway4.draw(win)

	win.getMouse()
	win.close()

es = cma.CMAEvolutionStrategy((numgate + numrunways) * [airport.centroid.coords[0][0], airport.centroid.coords[0][1], mingatelength, mingatewidth*100, 0], 1000)
es.optimize(fitness)
es.result_pretty()

result = es.result()[0]
print('[' + ', '.join(map(str,result)) + ']')
print(fitness(result))

gatepolygons = []
for i in range(numrunways, numrunways + numgate):
	x = result[i*5 + 0]
	y = result[i*5 + 1]
	#length = result[i*5 + 2]
	#width = result[i*5 + 3]/100
	length = mingatelength
	width = mingatewidth
	angle = result[i*5 + 4]/1000
	
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

allgates = gatepolygons[0]
for polygon in gatepolygons[1:]:
	allgates= allgates.union(polygon)
allgates= allgates.buffer(130)
gateperiphery = allgates.union(terminalbuilding).intersection(airport).boundary.difference(terminalbuilding.boundary).difference(airport.boundary)

numgates = gateperiphery.length / 45

for i in range(0, numgate):
	print("terminal %d:\n---------\nCenter: (%f, %f)\nLength: %f\nWidth: %f\nAngle: %f" % (i, result[i*5 + 0], result[i*5 + 1], result[i*5 + 2], result[i*5 + 3]/100, (((result[i*5 + 4]/1000) % math.pi) / 2 / math.pi * 360)))
print("Number of possible gates: %d" % numgates)
draw(result)

