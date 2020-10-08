import csv
import json
import pandas as pd
from pulp import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
from scipy.spatial.distance import euclidean
import random
import time
import sys
import geopy.distance
from geopy.distance import geodesic
import matplotlib.pyplot as plt



cutOffTime = 120
drone_endurance = 25
drone_cost = 1.0
# truck_cost = 25.0
truck_cost = 1.0

coordinates = [[28.6312756, 77.2239758], [28.6266846, 77.2397423], [28.6226552, 77.2092844], [28.6426552, 77.2792844], [28.6126542, 77.2292834]]


def distance_coordinates(coords_1, coords_2):
    d = geodesic(coords_1, coords_2).kilometers
    # print('coords ->',d)
    return d


def euclideanDist(node1: int, node2: int, coordinates: list) -> int:
    coord1 = coordinates[node1]
    coord2 = coordinates[node2]
    return distance_coordinates(coord1, coord2)


def generateDistanceMatrix(coordinates: list):
    distanceMatrix = []
    distanceMatrix.append(["City",'Depot','a', 'b', 'c', 'd'])
    city = ['Depot','a', 'b', 'c', 'd']
    cityCount = 0
    for i in range(len(coordinates)):
        matrix = []
        matrix.append(city[cityCount])
        for j in range(len(coordinates)):
            if i == j:
                matrix.append(0)
            else:
                matrix.append(euclideanDist(i, j, coordinates))
        distanceMatrix.append(matrix)
        cityCount += 1
    # distanceMatrix.append(distanceMatrix[0])
    return distanceMatrix


def flight_time(coordinates: list, drone_speed: float):
    distanceMatrix = []
    distanceMatrix.append(
        ["City", 'Depot','a', 'b', 'c', 'd'])
    city = ['Depot','a', 'b', 'c', 'd']
    cityCount = 0
    for i in range(len(coordinates)):
        matrix = []
        matrix.append(city[cityCount])
        for j in range(len(coordinates)):
            if i == j:
                matrix.append(0)
            else:
                matrix.append(euclideanDist(i, j, coordinates) / drone_speed)
        distanceMatrix.append(matrix)
        cityCount += 1
    # distanceMatrix.append(distanceMatrix[0])
    return distanceMatrix

def coordinateMatrix(coordinates: list):
    distanceMatrix = []
    distanceMatrix.append(["City","latitude","longitude"])
    cityCount = 0
    city = ['Depot','a', 'b', 'c', 'd']
    for i in city:
        distanceMatrix.append([i, coordinates[cityCount][0], coordinates[cityCount][1]])
        cityCount+=1
    # distanceMatrix.append(distanceMatrix[0])
    return distanceMatrix



matrix = generateDistanceMatrix(coordinates)
time_matrix = flight_time(coordinates, 0.01)
coordMatrix = coordinateMatrix(coordinates)

with open("distance.csv", "w") as d:
    writer = csv.writer(d)
    writer.writerows(matrix)

with open("time.csv", "w") as t:
    writer = csv.writer(t)
    writer.writerows(time_matrix)

with open("coordinates.csv", "w") as c:
    writer = csv.writer(c)
    writer.writerows(coordMatrix)


def nn(distanceMatrix: list, nodes: list):
    """Nearest Neighbour Path

    Args:
        distanceMatrix (list): Adjancency Matriz
        nodes (list): Contains node ID
    """
    nnTour = [nodes[0]]
    nnCost = 0.0
    unvisited_nodes = nodes
    nodes.pop(0)
    while(len(unvisited_nodes) > 0):
        top = nnTour[-1]
        temp = sys.maxsize
        index = 0
        for i in range(len(distanceMatrix[top])):
            if i == top:
                continue
            if ((distanceMatrix[top][i] < temp) and (unvisited_nodes.count(i) > 0)):
                temp = distanceMatrix[top][i]
                index = i
        # print('start -> ', temp)
        unvisited_nodes.remove(index)
        nnTour.append(index)
        nnCost += temp
    # we are now at the last city, and need to connect that back to the depot
    nnCost += distanceMatrix[nnTour[-1]][0]
    nnTour.append(0)
    return nnTour, nnCost



sites = ['Depot','a', 'b', 'c', 'd']
latlng = ['latitude', 'longitude']
position = pd.read_csv('./coordinates.csv', index_col="City") # coordinates
flighttime = pd.read_csv('./time.csv', index_col="City")
distance = pd.read_csv('./distance.csv', index_col="City")


#these are the coordinates of every city
positions = dict( ( city, (position.loc[city, 'longitude'], position.loc[city, 'latitude']) ) for city in sites)

for s in positions:
    p = positions[s]
    plt.plot(p[0],p[1],'o')
    plt.text(p[0]+.01,p[1],s,horizontalalignment='left',verticalalignment='center')
    
plt.gca().axis('off');


def ilp_model():
    """Kara, I., & Bektas, T. (2006). Integer linear programming formulations of multiple salesman problems
        and its variations. European Journal of Operational Research, 174(3), 1449–1458. 
        doi:10.1016/j.ejor.2005.03.008 
    """
    #a handful of sites
    sites = ['Barcelona','Belgrade','Depot','Brussels','Bucharest']
    latlng = ['latitude', 'longitude']
    position = pd.read_csv('./coordinates.csv', index_col="City")
    flighttime = pd.read_csv('./time.csv', index_col="City")
    distance = pd.read_csv('./distance.csv', index_col="City")
    # position.head(5)
    positions = dict( ( city, (position.loc[city, 'longitude'], position.loc[city, 'latitude']) ) for city in sites)

    # Plot
    for s in positions:
        p = positions[s]
        plt.plot(p[0],p[1],'o')
        plt.text(p[0]+.01,p[1],s,horizontalalignment='left',verticalalignment='center')
    
    plt.gca().axis('off');
    distances = dict( ((s1,s2), distance.loc[s1, s2] ) for s1 in positions for s2 in positions if s1!=s2)

    k = 2
    prob=LpProblem("vehicle", LpMinimize)
    #indicator variable if site i is connected to site j in the tour
    x = LpVariable.dicts('x',distances, 0,1, LpBinary)
    #dummy vars to eliminate subtours
    u = LpVariable.dicts('u', sites, 0, len(sites)-1, LpInteger)
    #the objective
    cost = lpSum([x[(i,j)]*distances[(i,j)] for (i,j) in distances])
    prob+=cost

    #constraints
    for k in sites:
        cap = 1 if k != 'Berlin' else K
        #inbound connection
        prob+= lpSum([ x[(i,k)] for i in sites if (i,k) in x]) ==cap
        #outbound connection
        prob+=lpSum([ x[(k,i)] for i in sites if (k,i) in x]) ==cap
    
    #subtour elimination
    N=len(sites)/K
    for i in sites:
        for j in sites:
            if i != j and (i != 'Berlin' and j!= 'Berlin') and (i,j) in x:
                prob += u[i] - u[j] <= (N)*(1-x[(i,j)]) - 1

    prob.solve()
    print(LpStatus[prob.status])

    non_zero_edges = [ e for e in x if value(x[e]) != 0 ]

    def get_next_site(parent):
        '''helper function to get the next edge'''
        edges = [e for e in non_zero_edges if e[0]==parent]
        for e in edges:
            non_zero_edges.remove(e)
        return edges
    tours = get_next_site('Berlin')
    tours = [ [e] for e in tours ]

    for t in tours:
        while t[-1][1] !='Berlin':
            t.append(get_next_site(t[-1][1])[-1])

    # the optimal path
    for t in tours:
        print(' -> '.join([ a for a,b in t]+['Berlin']))

    totalTime = 0;
    for t in tours:
        time = 0
        for i in range(0, len(t)):
            time += flighttime.loc[t[i][0], t[i][1]]
    #         print(flighttime.loc[t[i][0], t[i][1]])
    #     print(time)
        if time > totalTime:
            totalTime = time
    print(totalTime)

    #draw the tours
    colors = [np.random.rand(3) for i in range(len(tours))]
    for t,c in zip(tours,colors):
        for a,b in t:
            p1,p2 = positions[a], positions[b]
            plt.plot([p1[0],p2[0]],[p1[1],p2[1]], color=c)

    #draw the map again
    for s in positions:
        p = positions[s]
        plt.plot(p[0],p[1],'o')
        plt.text(p[0]+.01,p[1],s,horizontalalignment='left',verticalalignment='center')

    plt.title('%d '%K + 'people' if K > 1 else 'person')
    plt.xlabel('latitude')
    plt.ylabel('longitude')
    # plt.gca().axis('off')
    plt.show()

    print('Longest time spent:', totalTime, '(min)')
    print('Total distance:', value(prob.objective), '(km)')

# ilp_model()