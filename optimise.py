import cma

from draw import draw

def optimise(airport, fitness, makegatebuilding, es, printpreviousresult):
    logger = cma.CMADataLogger().register(es)
    
    ## Draw in in difrent filles
    if printpreviousresult:
        result = printpreviousresult
    else:
        es.optimize(fitness, logger=logger)
        es.result_pretty()
    
        result = es.result()[0]
        
    steps = logger.load().data()["xrecent"]
    
    i = 0
    while i < len(steps):
        print("%d of %d" % (i + 1, len(steps)))
        print(steps[i][5:])
        draw(airport, makegatebuilding, steps[i][5:], i)
        
        i += 1
#         if i < 100:
#             i += 1
#         elif i < len(steps) - 200:
#             i += 100
#         elif i < len(steps) - 20:
#             i += 10
#         else:
#             i += 1
    
    print('[' + ', '.join(map(str,result)) + ']')
    print(fitness(result))
    
    draw(airport, makegatebuilding, result)