import matplotlib.pyplot as plt
#import numpy as np

def createVoronoiPoints(): 
    #   
    centers = []

    def onclick(event):
        #
        nonlocal centers
        ex, ey = event.xdata, event.ydata 

        ax.plot(ex, ey, marker='o', linestyle='-', color='b')
        plt.show()

        centers.append( (ex, ey) )
        fig.canvas.draw()     
    #end procedure onclick()
    
    fig, ax = plt.subplots()
    ax.set_xlim((-100,100))
    ax.set_ylim((-100,100))
    ax.set_title("Draw centers of Voronoi-diagram")
    
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.grid()
    plt.show()
    
    return centers
#end procedure drawPolygon()
