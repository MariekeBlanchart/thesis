import cma, math, numpy

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

def shiftdown(m, i):
    return [m[x] for x in range(0, len(m)) if x >= i] + [m[x] for x in range(0, len(m)) if x < i]

def shiftright(m, i):
    transposed = [list(x) for x in zip(*m)]
    result = shiftdown(transposed, i)
    transposedback = [list(x) for x in zip(*result)]
    return transposedback

def tile (x):
    x = tobinary(x)
    result = 0

    r = to1dlist(shiftright(to2dlist(x), 1))
    errors = map(sum, zip(x, r))
    errors = filter(lambda i: i != 1, errors)
    result += len(errors)

    d = to1dlist(shiftdown(to2dlist(x), 1))
    errors = map(sum, zip(x, d))
    errors = filter(lambda i: i != 1, errors)
    result += len(errors)*1000



    return result

def fitness (x):
    x = tobinary(x)
    result = 0

    r = to1dlist(shiftright(to2dlist(x), 1))
    errors = map(sum, zip(x, r))
    errors = filter(lambda i: i != 1, errors)
    result += len(errors)

    d = to1dlist(shiftdown(to2dlist(x), 1))
    errors = map(sum, zip(x, d))
    errors = filter(lambda i: i != 1, errors)
    result += len(errors)

    return result

resultaten=[0]*10
#for y in range (1,11):
for x in range (0,10):
    es = cma.CMAEvolutionStrategy(16*[0],1)
    es.optimize(fitness)
    resultaten[x] = tile(es.result()[0])
#     if tile(es.result()[0])==0:
#         aantaljuist[0] +=1

for x in range (0,10):
    print(resultaten[x])



    

    