def gatefitness(airport, gatespolygon, agate_min, agate_max, pgate_min, pgate_max):
    
    res = 0
    
    if not gatespolygon:
        return 100000
    
    
    ## check if its a list, make a list
    if isinstance(gatespolygon, list):
        gatebuildings = gatespolygon
    else:
        try:
            gatebuildings = gatespolygon.geoms
        except AttributeError:
            gatebuildings = [gatespolygon]


    ## maesurements airport
    try:
        for gatebuilding in gatebuildings:
            if not airport.contains(gatebuilding) and gatebuilding.area:
                areaoutsideairport = 10*(10 + gatebuilding.difference(airport).area / gatebuilding.area * 100) # Percent of terminal that's outside airport
                res += areaoutsideairport
                
                if areaoutsideairport > 99:
                    # Try to guide terminal towards airportfield
                    res += airport.centroid.distance(gatebuilding.centroid)
        
        allgates = gatebuildings[0]
        for polygon in gatebuildings[1:]:
            allgates = allgates.union(polygon)
        totalarea = allgates.area
        allgates = allgates.buffer(130)
        totalperiphery = allgates.boundary.length
    
        if totalarea < agate_min:
            res += 10* (agate_min - totalarea)
        if  totalarea > agate_max:
            res += 10* (totalarea - agate_max)
        if totalperiphery < pgate_min:
            res += 10* (pgate_min - totalperiphery)
        if totalperiphery > pgate_max:
            res += 10* (totalperiphery - pgate_max)
        
        res += pgate_max - totalperiphery
        
        ##Kruskal's algorithm
        distances = []
        comp = {}
        totaldistance = 0
        #iteration over all the building
        for i in range(0, len(gatebuildings)):
            building1 = gatebuildings[i]
            comp[i] = {i}
            #iteration in an iteration to find the distance between 2 buildings    
            for j in range(i+1, len(gatebuildings)):
                building2 = gatebuildings[j]
                # make a list with distance between 2 buildings and building A an B, and later sort them on smallest distance
                distances.append((building1.distance(building2), i, j ))
        distances.sort()
        #iterate n - 1 times, with n = number of buildings
        for p in range(1, len(gatebuildings)):
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
         
    except:
        return 10000000
   
    return res