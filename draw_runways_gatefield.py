import shapely.geometry as geometry
import graphics
import math

def draw(airport, coords, numrunways, result_vormstrategie = None, mean_vormstrategie = None, construct_vormstrategie = None, filenamenum = None, merge=False):
	win = graphics.GraphWin('airport', 800, 800*(airport.bounds[3] - airport.bounds[1])/(airport.bounds[2] - airport.bounds[0])) # give title and dimensions
	win.setCoords(airport.bounds[0] - 10, airport.bounds[1] - 10, airport.bounds[2] + 10, airport.bounds[3] + 10)
	
	rectangle= graphics.Polygon(graphics.Point(-10000, -10000),graphics.Point(-10000, 10000),graphics.Point(10000, 10000),graphics.Point(10000, -10000))
	rectangle.setFill('black')
	rectangle.draw(win)

	airportgraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), airport.exterior.coords))
	airportgraphic.setFill('white')
	airportgraphic.draw(win)

	for i in range(0, numrunways + 1):
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
	
		x1 = x - width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y1 = y + width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x2 = x + width * math.sin(angle) / 2 + length * math.cos(angle) / 2
		y2 = y - width * math.cos(angle) / 2 + length * math.sin(angle) / 2
		
		x3 = x + width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y3 = y - width * math.cos(angle) / 2 - length * math.sin(angle) / 2
		
		x4 = x - width * math.sin(angle) / 2 - length * math.cos(angle) / 2
		y4 = y + width * math.cos(angle) / 2 - length * math.sin(angle) / 2
	
		runway = geometry.Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])
		
		runwayinside = runway.intersection(airport)
		runwayoutside = runway.difference(airport)
		
		try:
			runwayinside = runwayinside.geoms
		except AttributeError:
			runwayinside = [runwayinside]
			
		try:
			runwayoutside = runwayoutside.geoms
		except AttributeError:
			runwayoutside = [runwayoutside]
		
		for r in runwayinside:
			runwayinsidegraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), r.exterior.coords))
			runwayinsidegraphic.setOutline("black")
			runwayinsidegraphic.draw(win)
		
		for r in runwayoutside:
			runwayoutsidegraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), r.exterior.coords))
			runwayoutsidegraphic.setOutline("white")
			runwayoutsidegraphic.draw(win)

	if result_vormstrategie is not None:
		polygon_vormstrategie= construct_vormstrategie(result_vormstrategie)
		if isinstance(polygon_vormstrategie, list):
			gatebuildings = polygon_vormstrategie
		else:
			try:
				gatebuildings = polygon_vormstrategie.geoms
			except AttributeError:
				gatebuildings = [polygon_vormstrategie]
	
		if merge:
			mergedbuilding = gatebuildings[0]
			for gatebuilding in gatebuildings[1:]:
				mergedbuilding = mergedbuilding.union(gatebuilding)
			gatebuildings = [mergedbuilding]
			
		for gatebuilding in gatebuildings:
			if gatebuilding:
				gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), gatebuilding.exterior.coords))
				gatebuildinggraphic.setOutline("red")
				gatebuildinggraphic.draw(win)
				for interior in gatebuilding.interiors:
					gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), interior.coords))
					gatebuildinggraphic.setOutline("red")
					gatebuildinggraphic.draw(win)
	
		if mean_vormstrategie is not None:
			polygon_vormstrategie= construct_vormstrategie(mean_vormstrategie)
			if isinstance(polygon_vormstrategie, list):
				gatebuildings = polygon_vormstrategie
			else:
				try:
					gatebuildings = polygon_vormstrategie.geoms
				except AttributeError:
					gatebuildings = [polygon_vormstrategie]
				
			for gatebuilding in gatebuildings:
				if gatebuilding:
					gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), gatebuilding.exterior.coords))
					gatebuildinggraphic.setOutline("grey")
					gatebuildinggraphic.draw(win)
					for interior in gatebuilding.interiors:
						gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), interior.coords))
						gatebuildinggraphic.draw(win)

	if filenamenum is not None:
		win.postscript(file="output/step-%05d.ps" % filenamenum, colormode='color')
	else:
		win.postscript(file="output/stepfinal.ps", colormode='color')
		win.getMouse()
	win.close()