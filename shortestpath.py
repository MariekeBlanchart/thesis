from graphics import*
import cma, numpy, math

##start blok
(a,b)=(5, 0)

##end blok
(c,d)=(5,9)

##not through blok
black=[(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(9,5),
       (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),
       (6,3),(2,4)]

maxx = 9
maxy = 9

def tomatrix(x):
    matrix = numpy.matrix(x)
    matrix = numpy.reshape(matrix, (-1, int(math.sqrt(len(x)))))
    return matrix

def to1dlist(x):
    return sum(x, [])

def to2dlist(x):
    return tomatrix(x).tolist()

def tobinary(x):
    return map(lambda i: 1 if i > 0 else 0, x)
    
def opmaak(h):
    h = to2dlist(tobinary(h))
    win = GraphWin('grid', 800, 800) # give title and dimensions

    
    for i in range (0,maxx+1):
        for j in range (0,maxy+1):
            rect = Rectangle(Point(i*80, j*80), Point(i*80+80, j*80+80))
            if h[i][j]:
                rect.setFill('blue')
            if i == a and j == b:
                rect.setFill('green')
            if i== c and j == d:
                rect.setFill('red')
            if (i, j) in black:
               rect.setFill('black')
            if (i, j) in black and h[i][j]:
                rect.setFill('yellow')
            rect.draw(win)
        
    win.getMouse()
    win.close()

def findpath (grid):
    root= (a,b)
    endpoint = (c,d)
    visited = [root]
    tree = [root]
    current = root
    if not grid[root[0]][root[1]]:
        return False
    while True:
        if current == endpoint:
            return True
        else :
            found = False
            while not found:
                found = True
                if current[0] + 1 <= maxx and (current[0] +1, current[1]) not in visited and grid[current[0] +1][current[1]]:
                    current = (current[0] +1, current[1])
                elif current[1] + 1 <= maxy and (current[0], current[1]+1) not in visited and grid[current[0]][current[1]+1]:
                    current = (current[0], current[1]+1)
                elif current[0] - 1 >= 0 and (current[0] -1, current[1]) not in visited and grid[current[0] -1][current[1]]:
                    current = (current[0] -1, current[1])
                elif current[1] - 1 >= 0 and (current[0], current[1]-1) not in visited and grid[current[0]][current[1]-1]:
                    current = (current[0], current[1]-1)
                else: 
                    found = False
                    
                if found:
                    visited.append(current)
                    tree.append(current)
                else:
                    tree.pop()
                    if not tree:
                        return False
                    current = tree[-1]
                
                    

def fitness(x):
    x = tobinary(x)
    x2d = to2dlist(x)
    result = 0
    
    if not findpath(x2d):
        result+=10000000
    
    for (i,j) in black:
        if x2d[i][j]:
            result+=100000
    
    result += sum (x)

    
    return result

es = cma.CMAEvolutionStrategy(100*[1], 2)
es.optimize(fitness)
es.result_pretty()
opmaak(es.result()[0])
