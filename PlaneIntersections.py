import math 
from collections import deque 
from visualizer.main import Visualizer
import numpy as np 

# Łukasz Klon, Filip Pawłowicz
# Diagramy Voronoi'a - projekt

def pointIntersection(segmentA, segmentB):
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

def Dot(segmentA, segmentB):
    pointA, pointB = segmentA 
    pointC, pointD = segmentB

    ax, ay = pointB[1] - pointA[1], pointB[0] - pointA[0]
    bx, by = pointD[1] - pointC[1], pointD[0] - pointC[0]

    return ax * bx + ay * by 
# end procedure Dot()

def Cross(segmentA, segmentB):
    #
    pointA, pointB = segmentA 
    pointC, pointD = segmentB

    ax, ay = pointB[1] - pointA[1], pointB[0] - pointA[0]
    bx, by = pointD[1] - pointC[1], pointD[0] - pointC[0]

    return ax * by - bx * ay 
# end procedure Cross()
    
def Orientation(A, B, C):
    #
    ax, ay = A 
    bx, by = B 
    cx, cy = C 

    answer = (ax - cx) * (by - cy) - (ay - cy) * (bx - cx)
    return answer
# end procedure Orientation()

def isOutsideHalfPlane(halfplane, point):
    #
    pointA, pointB = halfplane 
    return Orientation(pointA, pointB, point) < 0
# end procedure isOutsideHalfPlane()

def Partition(sections, left, right):
#
    a = left - 1 
    for b in range(left, right):

        pointA, pointB = sections[b]
        pointC, pointD = sections[right]

        # if math.atan2( pointB[0] - pointA[0], pointB[1] - pointA[1] ) < math.atan2( pointD[0] - pointC[0], pointD[1] - pointC[1] ):
        if math.atan2( pointB[1] - pointA[1], pointB[0] - pointA[0] ) < math.atan2( pointD[1] - pointC[1], pointD[0] - pointC[0] ):
            a += 1 
            sections[a], sections[b] = sections[b], sections[a]
    #
            
    sections[a + 1], sections[right] = sections[right], sections[a + 1] 
    return a + 1 
# end procedure Partition()

def QuickSort(sections, left, right):
#
    if left < right:
        pivot = Partition(sections, left, right)
        QuickSort(sections, left, pivot - 1)
        QuickSort(sections, pivot + 1, right) 
    # 
# end procedure QuickSort()
        
def sortByAngle(lines):
    #
    QuickSort(lines, 0, len(lines) - 1)
    return lines 
# end procedure sortByAngle()
            

def halfPlanesIntersections(halfPlanes):
    #
    INF = 100
    bigBox = [ (INF, INF), (-INF, INF), (-INF, -INF), (INF, -INF) ]
    for idx in range(4):
        halfPlanes.append( (bigBox[idx], bigBox[ (idx + 1) % 4] ) )
    #

    halfPlanes = sortByAngle(halfPlanes)
    queue = deque()

    # for line in bigBox: queue.append(line)

    for a in range( len(halfPlanes) ):

        halfPlane = halfPlanes[a] 

        while len(queue) > 1 and isOutsideHalfPlane(halfPlane, pointIntersection( queue[-1], queue[-2] )):
            queue.pop()
        #
        
        while len(queue) > 1 and isOutsideHalfPlane(halfPlane, pointIntersection( queue[0], queue[1] )):
            queue.popleft()
        #
        
        if len(queue) > 0 and abs( Cross(halfPlane, queue[-1]) ) < 10 ** (-9):
            #
            if Dot( halfPlane, queue[-1] ) < 0: 
                return []
            
            if isOutsideHalfPlane(halfPlane, queue[-1][0]):
                queue.pop()
            
            else: continue 
        # end 'if' clause 
            
        queue.append(halfPlane)
    # end 'for' loop 
    
    halfPlane = queue[0] 
    while len(queue) > 2 and isOutsideHalfPlane( halfPlane, pointIntersection( queue[-1], queue[-2] ) ):
        queue.pop() 
    #
    
    halfPlane = queue[-1] 
    while len(queue) > 2 and isOutsideHalfPlane( halfPlane, pointIntersection( queue[0], queue[1] ) ):
        queue.popleft()
    #
    
    return list(queue) 
# end procedure halfPlaneIntersections()
