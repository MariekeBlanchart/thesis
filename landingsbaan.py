import graphics
import shapely.geometry as geometry
import cma, math


airport = geometry.Polygon([(0,0), (500, 1000), (2500, 1000), (1500, 3000), (0, 3000)])

minrunwaylength = 2700
minrunwaywidth = 40

numrunways = 2
preferredangledegrees = [60,60]
usedtogether = [[1],[0]]


preferredangle = []
for i in range(0, numrunways):
	preferredangle.append(1.0 * (preferredangledegrees[i] % 180) / 360 * 2*math.pi)

def fitness(coords):
	res = 0
	polygons = []
	
	for i in range(0, numrunways):
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		length = coords[i*5 + 2]
		width = coords[i*5 + 3]/100
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
		
		if not airport.contains(polygon):
			try:
				areaoutsideairport = 10 + polygon.difference(airport).area / polygon.area * 100 # Percent of runway that's outside airport
			except:
				print "Error: (%d %d) (%d %d) (%d %d) (%d %d) %d %d" % (x1, y1, x2, y2, x3, y3, x4, y4, length, width)
			res += areaoutsideairport
			
			if areaoutsideairport > 99:
				# Try to guide runway towards airport
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
		
		polygons.append(polygon)

	for i in range(0, numrunways):
		for j in usedtogether[i]:
			if polygons[i].intersects(polygons[j]):
				res += (10 + polygons[i].intersection(polygons[j]).area)
	
	return res

def draw(coords):
	win = graphics.GraphWin('airport', 600, 600*(airport.bounds[3] - airport.bounds[1])/(airport.bounds[2] - airport.bounds[0])) # give title and dimensions
	win.setCoords(airport.bounds[0] - 10, airport.bounds[1] - 10, airport.bounds[2] + 10, airport.bounds[3] + 10)

	airportgraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), airport.exterior.coords))
	airportgraphic.draw(win)
	
	colours = {
		0: "red",
		1: "blue",
		2: "green",
		3: "yellow",
		4: "magenta",
		5: "cyan",
	}
	
	for i in range(0, numrunways):
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		length = coords[i*5 + 2]
		width = coords[i*5 + 3]/100
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

es = cma.CMAEvolutionStrategy(numrunways*[airport.centroid.coords[0][0], airport.centroid.coords[0][1], minrunwaylength, minrunwaywidth*100, 0], 1000)
es.optimize(fitness)
es.result_pretty()

result = es.result()[0]
print(fitness(result))
for i in range(0, numrunways):
	print("Runway %d:\n---------\nCenter: (%f, %f)\nLength: %f\nWidth: %f\nAngle: %f" % (i, result[i*5 + 0], result[i*5 + 1], result[i*5 + 2], result[i*5 + 3]/100, (((result[i*5 + 4]/1000) % math.pi) / 2 / math.pi * 360)))
draw(result)
