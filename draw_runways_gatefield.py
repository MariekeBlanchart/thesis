import shapely.geometry as geometry
import graphics
import math

def draw(airport, coords, numrunways, result_vormstrategie = None, mean_vormstrategie = None, construct_vormstrategie = None, filenamenum = None, ofnum = None, merge=False):
	win = graphics.GraphWin('airport', 1040, 800) # give title and dimensions
	airportwidth = airport.bounds[2] - airport.bounds[0] + 1000
	airportheight = airport.bounds[3] - airport.bounds[1] + 200
	maxdimension = max(airportwidth / 13, airportheight / 10)
	win.setCoords(airport.bounds[0] - (maxdimension * 13 - airportwidth)/2 - 500,
				  airport.bounds[1] - (maxdimension * 10 - airportheight)/2 - 100,
				  airport.bounds[2] + (maxdimension * 13 - airportwidth)/2 + 500,
				  airport.bounds[3] + (maxdimension * 10 - airportheight)/2 + 100)
	
	rectangle= graphics.Polygon(graphics.Point(-100000, -100000),graphics.Point(-100000, 100000),graphics.Point(100000, 100000),graphics.Point(100000, -100000))
	rectangle.setFill('#869685')
	rectangle.draw(win)

	airportgraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), airport.exterior.coords))
	airportgraphic.setFill('white')
	airportgraphic.draw(win)
	
	###scale 5 blokje
	ymin = airport.bounds[1] - 10
	if airportwidth / airportheight < 0.79:
		xmax = airport.bounds[2] + 10 + 500
	else:
		xmax = airport.bounds[2] + 10 - 200
	heightbox= 50
	widthbox = 100
	
	for i in range(0, 5):
		rectangle = graphics.Polygon(graphics.Point(xmax - widthbox, ymin + heightbox),
									 graphics.Point(xmax,            ymin + heightbox),
									 graphics.Point(xmax,            ymin),
									 graphics.Point(xmax - widthbox, ymin))
		rectangle.setFill("gray" if i % 2 else "white")
		rectangle.draw(win)
		xmax -= widthbox
	
	## Compass rose
	
	if ofnum:
		##numbre of iterations
		label = graphics.Text(graphics.Point(xmax + widthbox+140, ymin + heightbox + 100), "%d of %d" % (filenamenum + 1 if filenamenum else ofnum, ofnum))
		label.setFill("gray")
		label.draw(win)

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
				if not filenamenum:
					gatebuildinggraphic.setFill("grey")
				gatebuildinggraphic.setOutline("black")
				gatebuildinggraphic.draw(win)
				for interior in gatebuilding.interiors:
					gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), interior.coords))
					gatebuildinggraphic.setFill("white")
					gatebuildinggraphic.setOutline("black")
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
					if not filenamenum:
						gatebuildinggraphic.setFill("grey")
					gatebuildinggraphic.setOutline("black")
					gatebuildinggraphic.draw(win)
					for interior in gatebuilding.interiors:
						gatebuildinggraphic = graphics.Polygon(map(lambda (x, y): graphics.Point(x,y), interior.coords))
						gatebuildinggraphic.setFill("white")
						gatebuildinggraphic.setOutline("black")
						gatebuildinggraphic.draw(win)

	if filenamenum is not None:
		win.postscript(file="output/step-%05d.ps" % filenamenum, colormode='color')
	else:
		win.postscript(file="output/stepfinal.ps", colormode='color')
		win.getMouse()
	win.close()