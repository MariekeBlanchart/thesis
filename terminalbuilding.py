import graphics
import shapely.geometry as geometry
import cma, math


airport = geometry.Polygon([(0,0), (500, 1000), (2500, 1000), (1500, 3000), (0, 3000)])

terminallenghtx= 300
terminalwidthy= 90
beginpointx = 1000
beginpointy = 1000

terminalbuilding = geometry.Polygon([(beginpointx,beginpointy),(beginpointx+terminallenghtx,beginpointy),(beginpointx+terminallenghtx,beginpointy+terminalwidthy),(beginpointx,beginpointy+terminalwidthy) ])

mingatelength = 650
mingatewidth = 60

numgate = 5


def fitness(coords):
	res = 0
	polygons = []
	
	for i in range(0, numgate):
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		#length = coords[i*5 + 2]
		#width = coords[i*5 + 3]/100
		length = 650
		width = 60
		angle = coords[i*5 + 4]/1000
		
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
		polygons.append(polygon)
		
		if not airport.contains(polygon):
			try:
				areaoutsideairport = 10 + polygon.difference(airport).area / polygon.area * 100 # Percent of terminal that's outside airport
			except:
				print "Error: (%d %d) (%d %d) (%d %d) (%d %d) %d %d" % (x1, y1, x2, y2, x3, y3, x4, y4, length, width)
			res += areaoutsideairport
			
			if areaoutsideairport > 99:
				# Try to guide terminal towards airport
				res += airport.centroid.distance(polygon.centroid)
			
		if length < mingatelength:
			res += (10 + mingatelength - length)
		if length > mingatelength:	
			res += (10 - mingatelength + length)
			
		if width < mingatewidth:
			res += (10 + mingatewidth - width)
		if width > mingatewidth:
			res += (10 - mingatewidth + width)

	allgates = polygons[0]
	for polygon in polygons[1:]:
		allgates= allgates.union(polygon)
	allgates= allgates.buffer(130)
	gateperiphery = allgates.union(terminalbuilding).intersection(airport).boundary.difference(terminalbuilding.boundary).difference(airport.boundary)

	res -= gateperiphery.length / 5
	
	##Kruskal's algorithm
	distances = []
	comp = {}
	totaldistance = 0
	
	#iteration over all the building
	for i in range(-1, len(polygons)):
		if i >= 0:
			building1 = polygons[i]
		else:
			building1 = terminalbuilding
		comp[i] = {i}
		
		#iteration in an iteration to find the distance between 2 buildings	
		for j in range(i+1, len(polygons)):
			building2 = polygons[j]
			# make a list with distance between 2 buildings and building A an B, and later sort them on smallest distance
			distances.append((building1.distance(building2), i, j ))
	distances.sort()

	#iterate n - 1 times, with n = number of buildings
	for p in range(1, len(polygons)+1):
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
	
	for i in range(0, numgate):
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		#length = coords[i*5 + 2]
		#width = coords[i*5 + 3]/100
		length = 650
		width = 60
		angle = coords[i*5 + 4]/1000
		colour = colours.get(i, "black")
		
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

es = cma.CMAEvolutionStrategy(numgate*[airport.centroid.coords[0][0], airport.centroid.coords[0][1], mingatelength, mingatewidth*100, 0], 1000)
es.optimize(fitness)
es.result_pretty()

result = es.result()[0]
print('[' + ', '.join(map(str,result)) + ']')
print(fitness(result))

polygons = []
for i in range(0, numgate):
	x = result[i*5 + 0]
	y = result[i*5 + 1]
	#length = result[i*5 + 2]
	#width = result[i*5 + 3]/100
	length = 650
	width = 60
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
	polygons.append(polygon)

allgates = polygons[0]
for polygon in polygons[1:]:
	allgates= allgates.union(polygon)
allgates= allgates.buffer(130)
gateperiphery = allgates.union(terminalbuilding).intersection(airport).boundary.difference(terminalbuilding.boundary).difference(airport.boundary)

numgates = gateperiphery.length / 45

for i in range(0, numgate):
	print("terminal %d:\n---------\nCenter: (%f, %f)\nLength: %f\nWidth: %f\nAngle: %f" % (i, result[i*5 + 0], result[i*5 + 1], result[i*5 + 2], result[i*5 + 3]/100, (((result[i*5 + 4]/1000) % math.pi) / 2 / math.pi * 360)))
print("Number of possible gates: %d" % numgates)
draw(result)
