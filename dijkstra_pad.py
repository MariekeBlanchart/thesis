from collections import *
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

def opmaak(path):
    win = GraphWin('grid', 800, 800) # give title and dimensions
    
    for i in range (0,maxx+1):
        for j in range (0,maxy+1):
            rect = Rectangle(Point(i*80, j*80), Point(i*80+80, j*80+80))
            if (i, j) in path:
                rect.setFill('blue')
            if i == a and j == b:
                rect.setFill('green')
            if i== c and j == d:
                rect.setFill('red')
            if (i, j) in black:
                rect.setFill('black')
            if (i, j) in black and (i,j) in path:
                rect.setFill('yellow')
            rect.draw(win)
        
    win.getMouse()
    win.close()

def dijkstra ():
    distances = [[1000000000 for i in range(10)] for j in range(10)]
    print(distances)
    distances[a][b] = 0
    print(a)
    print(b)
    print(distances)
    temp=[(i,j) for i in range(0,10) for j in range(0,10) if (i,j) not in black]
    previous = [[(0,0) for i in range(10)] for j in range(10)]
    while temp:
        minimum=100000000
        (mini, minj)=(0,0)
        for (i,j) in temp:
            if distances[i][j]<minimum: 
                minimum= distances[i][j]
                (mini, minj)=(i,j)
            
        temp.remove((mini,minj))
        
        if mini+1 <= maxx and distances [mini+1][minj] > minimum +1:
            distances [mini+1][minj] = minimum +1
            previous [mini+1][minj] =(mini, minj)
            
        if mini-1 >= 0 and distances [mini-1][minj] > minimum +1:
            distances [mini-1][minj] = minimum +1
            previous [mini-1][minj] =(mini, minj)
            
        if minj+1 <= maxy and distances [mini][minj+1] > minimum +1:
            distances [mini][minj+1] = minimum +1
            previous [mini][minj+1] =(mini, minj)
                
        if minj-1 >= 0 and distances [mini][minj-1] > minimum +1:
            distances [mini][minj-1] = minimum +1
            previous [mini][minj-1] =(mini, minj)
    
    passed=[(c,d)]
    cnt = 0
    while passed [-1] != (a,b) and cnt < 1000:
        (x,y) = passed[-1]
        passed.append(previous[x][y])
        cnt += 1
        
    return passed

opmaak(dijkstra())