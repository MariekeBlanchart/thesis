import matplotlib.pyplot as plt

def draw_plots (fitnessnumbers):
    plt.figure()
    plt.plot([x - min(fitnessnumbers) + 0.00000001 for x in fitnessnumbers])
    plt.ylabel('Fitness')
    plt.yscale('log')
    plt.show()