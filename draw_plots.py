import matplotlib.pyplot as plt

def draw_plots (fitnessnumbers):
    plt.figure()
    plt.plot(fitnessnumbers, 'g')
    minimum = min(fitnessnumbers)
    minimum2 = min2(fitnessnumbers)
    plt.plot([x- minimum + (minimum2 - minimum)   for x in fitnessnumbers], 'b')
    plt.title('Optimalisatie van een landingsbaan')
    plt.xlabel('Generatie')
    plt.ylabel('Fitness')
    plt.yscale('log')
    plt.show()
    
def min2(ns):
    m = min(ns)
    return min([n for n in ns if n > m])