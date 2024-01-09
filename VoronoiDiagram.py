from PlaneIntersections import halfPlanesIntersections
from visualizer.main import Visualizer 
from generatePoints import createVoronoiPoints

def Orientation(A, B, C):
    #
    ax, ay = A 
    bx, by = B 
    cx, cy = C 

    answer = (ax - cx) * (by - cy) - (ay - cy) * (bx - cx)
    return answer
# end procedure Orientation()

def segmentIntersection(segmentA, segmentB):
    #
    (ax, ay), (bx, by) = segmentA
    (cx, cy), (dx, dy) = segmentB
    
    # Ax + By + C = 0 
    if bx - ax == 0: 
        A = 1 
        B = 0 
        C = -ax
    else:

        a1 = (by - ay) / (bx - ax) 
        b1 = ay - a1 * ax 

        A = -a1
        B = 1 
        C = -b1

    # Dx + Ey + F = 0 
    if dx - cx == 0:
        D = 1 
        E = 0 
        F = -cx 
    else:

        a2 = (dy - cy) / (dx - cx) 
        b2 = cy - a2 * cx 

        D = -a2 
        E = 1 
        F = -b2
    #

    x = (B * F - E * C) / (A * E - D * B)
    y = (D * C - A * F) / (A * E - D * B)

    return (x, y)
# end procedure pointIntersection()

def Partition(points, left, right, centerPoint):
    #
    a = left - 1

    for b in range(left, right): 
        if Orientation( centerPoint, points[right], points[b] ) < 0: 
            a += 1 
            points[a], points[b] = points[b], points[a] 
        #
    # end 'for' loop 
    
    points[a + 1], points[right] = points[right], points[a + 1]
    return a + 1 
# end procedure Partition() 

def QuickSort(points, left, right, centerPoint):
    #
    if left < right: 
        pivot = Partition(points, left, right, centerPoint)
        QuickSort(points, left, pivot - 1, centerPoint) 
        QuickSort(points, pivot + 1, right, centerPoint) 
    #
# end procedure QuickSort()
        
def sortCounterClockWise(points):
    #
    n = len(points)

    sumX, sumY = 0, 0
    for (x, y) in points:
        sumX += x 
        sumY += y 
    # 
        
    centerX, centerY = sumX / n, sumY / n 
    QuickSort( points, 0, len(points) - 1, (centerX, centerY) )

    return points 
# end procedure sortCounterClockWise() 

def createSections(point, points):
    #
    sections = [] 

    for neighbour in points:
        if point == neighbour: continue 

        (a1,b1) = point 
        (a2,b2) = neighbour 

        if abs( b2 - b1 ) < 10 ** (-9):
            mid = (a1 + a2) / 2 
    
            if Orientation( (mid, b2 + 10), (mid, b2 - 10), point ) > 0:
                sections.append( ( (mid, b2 + 10), (mid, b2 - 10) ) ) 
            else:
                sections.append( ( (mid, b2 - 10), (mid, b2 + 10) ) ) 

        else:

            slope = (a1 - a2) / (b2 - b1) 
            intercept = 0.5 * (b1 + b2 - (a1 - a2) * (a1 + a2) / (b2 - b1) ) 

            if Orientation( (-10, slope * (-10) + intercept), (10, slope * (10) + intercept), point ) < 0:
                sections.append( ( (10, slope * (10) + intercept), (-10, slope * (-10) + intercept ) ) ) 
            else:
                sections.append( ( (-10, slope * (-10) + intercept), (10, slope * (10) + intercept ) ) ) 
    # 

    return sections 
# end procedure createSections()

def intersectionHalfPlanesPoints(halfPlanes):
    #
    cross = [] 

    for idx in range( len(halfPlanes) ):
        segmentA, segmentB = halfPlanes[idx], halfPlanes[ (idx + 1) % len(halfPlanes) ]
        intersection = segmentIntersection(segmentA, segmentB)
        cross.append(intersection)
    # end 'for' loop 

    cross = sortCounterClockWise(cross)

    return cross 
# end procedure intersectionHalfPlanesPoints()

def getNextColor(counter):
    #
    colors  = [ "blue", "orange", "green", "red", "purple", "brown", "pink", "olive", "tomato", "sienna", "darkorange", "wheat", "gold", "olive", "greenyellow", "lightgreen", "turquoise", "azure", "darkcyan", "deepskyblue", "lightslategray", "mediumslateblue", "indigo", "darkorchid", "violet", "deeppink", "crimson" ]
    return colors[ counter % len(colors) ]
# end procedure getNextColor()

from random import randint 
import numpy as np 

def change(point):
    #
    x, y = point 
    x = randint(-4, 4) + x 
    y = randint(-4, 4) + y 
    return (x,y)
# 

def VoronoiDiagram():
    #
    vis = Visualizer()
    vis.axis_equal()
    counter = 0 

    centers = createVoronoiPoints()
    # centers = [ (-4,-2), (3,5), (0,0), (1,1), (3,-3) ]
    
    for center in centers:
        #
        halfPlanes         = createSections(center, centers)

        boxVoronoiSegments = halfPlanesIntersections(halfPlanes)
        boxVoronoiPoints   = intersectionHalfPlanesPoints(boxVoronoiSegments)
        
        vis.add_polygon( boxVoronoiPoints, color = getNextColor(counter) )
        # vis.add_polygon( boxVoronoiPoints, fill = False )
        counter += 1
    # end 'for' loop 
    
    vis.add_point(centers, color = "black", s = 15)
    vis.show()
# end procedure VoronoiDiagram()
    
VoronoiDiagram()




