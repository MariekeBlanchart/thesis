import graphics
import math

def draw(airport, makegatebuilding, coords, numrunways, filenamenum = None):
	win = graphics.GraphWin('airport', 600, 600*(airport.bounds[3] - airport.bounds[1])/(airport.bounds[2] - airport.bounds[0])) # give title and dimensions
	win.setCoords(airport.bounds[0] - 10, airport.bounds[1] - 10, airport.bounds[2] + 10, airport.bounds[3] + 10)

	airportgraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), airport.exterior.coords))
	airportgraphic.draw(win)

	for i in range(0, numrunways):
		x = coords[i*5 + 0]
		y = coords[i*5 + 1]
		length = coords[i*5 + 2]
		width = coords[i*5 + 3]/100
		angle = coords[i*5 + 4]/1000
		colour = "black"
	
		x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x2 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y2 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		x3 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y3 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
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
	
	gatespolygon = makegatebuilding(coords[numrunways*5:])
	
	try:
		gatebuildings = gatespolygon.geoms
	except AttributeError:
		gatebuildings = [gatespolygon]
		
	for gatebuilding in gatebuildings:
		if gatebuilding:
			gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), gatebuilding.exterior.coords))
			gatebuildinggraphic.draw(win)
			for interior in gatebuilding.interiors:
				gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), interior.coords))
				gatebuildinggraphic.draw(win)

	if filenamenum is not None:
		win.postscript(file="output/step-%05d.ps" % filenamenum, colormode='color')
	else:
		win.getMouse()
	win.close()
