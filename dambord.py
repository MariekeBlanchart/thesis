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

    sumx=sum(x)
    if sumx < len(x)/2:
        result -= sumx
    else:
        result -= len(x)-sumx

    r = to1dlist(shiftright(to2dlist(x), 1))
    errors = map(sum, zip(x, r))
    errors = filter(lambda i: i != 1, errors)
    result += len(errors)

    d = to1dlist(shiftdown(to2dlist(x), 1))
    errors = map(sum, zip(x, d))
    errors = filter(lambda i: i != 1, errors)
    result += len(errors)

    return result

es = cma.CMAEvolutionStrategy(9* [0], 0.5)
es.optimize(tile)
es.result_pretty()
es.plot()
cma.savefig("plot.png")
cma.closefig()

print(tomatrix(tobinary(es.result()[0])))
