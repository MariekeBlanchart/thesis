import cma, math, numpy

def inputt (x):
    word = "Shakespeare"
    result = 0
    
    for i in range(0,len(word)):
        char= ord(word[i])   
        char2 = x[i]
        result += abs(char- char2)
    
    return result

resultaten= [0]*10
for i in range(0,10):
    es = cma.CMAEvolutionStrategy(11*[0], 13)
    es.optimize(inputt)
    es.result_pretty()
    resultaten[i] = map(lambda x: chr(int(round(x))), es.result()[0])
    
for i in range(0,10):
    print(resultaten[i])

