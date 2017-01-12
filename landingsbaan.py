from graphics import *
from shapely.geometry import Polygon
import cma, math


airportlength = 4000
airportwidth = 2500

minrunwaylength = 2700
minrunwaywidth = 40

scale = 10
border = 10

numrunways = 2
preferredangledegrees = [90,90]
usedtogether = [[], []]


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
		width = coords[i*5 + 3]
		angle = coords[i*5 + 4]
		
		if length < 0:
			res += -length
		
		if width < 0:
			res += -width
		
		x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		if x1 < 0 or x2 < 0 or x3 < 0 or x4 < 0:
			res += (1+(0-min(x1,x2,x3,x4)))
			
		if x1 > airportlength or x2 > airportlength or x3 > airportlength or x4 > airportlength:
			res += (1+(max(x1,x2,x3,x4)-airportlength))
				
		if y1 < 0 or y2 < 0 or y3 < 0 or y4 < 0:
			res += (1+(0-min(y1,y2,y3,y4)))
			
		if y1 > airportwidth or y2 > airportwidth or y3 > airportwidth or y4 > airportwidth:
			res += (1+(max(y1,y2,y3,y4)-airportwidth))
			
		if length < minrunwaylength:
			res += (1 + minrunwaylength-length)
			
		if width < minrunwaywidth:
			res += (1 + minrunwaywidth-width)
	
		angle = angle % math.pi
		
		if (angle < preferredangle[i]):
			res += preferredangle[i] - angle
		else:
			res += angle - preferredangle[i]
		
		polygons.append(Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]))

	for i in range(0, numrunways):
		for j in usedtogether[i]:
			if polygons[i].intersects(polygons[j]):
				res += (1 + polygons[i].intersection(polygons[j]).area)
	
	return res

def draw(coords):
	win = GraphWin('airport', 600, 600) # give title and dimensions
	win.setCoords(-10, -10, max(airportlength, airportwidth) + 10, max(airportlength, airportwidth) + 10)

	airport = Rectangle(Point(0, 0), Point(airportlength, airportwidth))
	airport.draw(win)

	colours = {
		0: "red",
		1: "blue",
		2: "green"
	}
	
	for i in range(0, numrunways):
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		length = coords[i*5 + 2]
		width = coords[i*5 + 3]
		angle = coords[i*5 + 4]
		colour = colours.get(i, "black")
		
		x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
	
		runway1 = Line(Point(x1, y1), Point(x2, y2))
		runway1.setOutline(colour)
		runway1.draw(win)
		runway2 = Line(Point(x2, y2), Point(x3, y3))
		runway2.setOutline(colour)
		runway2.draw(win)
		runway3 = Line(Point(x3, y3), Point(x4, y4))
		runway3.setOutline(colour)
		runway3.draw(win)
		runway4 = Line(Point(x4, y4), Point(x1, y1))
		runway4.setOutline(colour)
		runway4.draw(win)

	win.getMouse()
	win.close()

es = cma.CMAEvolutionStrategy(numrunways*[airportlength / 2, airportwidth / 2, airportlength, 5, 0], 10)
es.optimize(fitness)
es.result_pretty()

result = es.result()[0]
for i in range(0, numrunways):
	print("Runway %d:\n---------\nCenter: (%f, %f)\nLength: %f\nWidth: %f\nAngle: %f" % (i, result[i*5 + 0], result[i*5 + 1], result[i*5 + 2], result[i*5 + 3], ((result[i*5 + 4] % math.pi) / 2 / math.pi * 360)))
draw(result)