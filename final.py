import csv
import json
import pandas as pd
from typing import List, Tuple
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
# from tsp import kMeansNodes


# cutOffTime = 120
# drone_endurance = 25
# drone_cost = 1.0
# # truck_cost = 25.0
# truck_cost = 1.0

coordinates = [[28.6312756, 77.2239758], [28.6266846, 77.2397423], [
    28.6226552, 77.2092844], [28.6426552, 77.2792844], [28.6126542, 77.2292834]]


def distance_coordinates(coords_1, coords_2) -> float:
    """Find Distance between 2 coordinates

    Args:
        coords_1 (list): coordinate
        coords_2 (list): coordinate

    Returns:
        distance (int): Distance between 2 points
    """
    return geodesic(coords_1, coords_2).kilometers


def euclideanDist(node1: int, node2: int, coordinates: list) -> float:
    """FInd the euclidean distance between 2 points

    Args:
        node1 (int): cityNode
        node2 (int): cityNode
        coordinates (list): Coordinates

    Returns:
        int: distance
    """
    coord1 = coordinates[node1]
    coord2 = coordinates[node2]
    return distance_coordinates(coord1, coord2)


def generateDistanceMatrix(coordinates: List[float]) -> List[List[float]]:
    """Generate Adjacency Matrix

    Args:
        coordinates (list): coordinates

    Returns:
        matrix: 2D lists
    """
    distanceMatrix = [['City', 'Depot']]
    alpha = 'a'
    for i in range(len(coordinates) - 1):
        distanceMatrix[0].append(alpha)
        alpha = chr(ord(alpha) + 1)
    city = distanceMatrix[0].copy()
    city.remove('City')
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
    openFiles("distance.csv", distanceMatrix)
    return distanceMatrix


def flight_time(coordinates: List[float], drone_speed: float) -> None:
    """Generate the flight time matrix

    Args:
        coordinates (list): list of coordinates
        drone_speed (float): speed of drone in kmph
    """
    distanceMatrix = [['City', 'Depot']]
    alpha = 'a'
    for i in range(len(coordinates) - 1):
        distanceMatrix[0].append(alpha)
        alpha = chr(ord(alpha) + 1)
    city = distanceMatrix[0].copy()
    city.remove('City')
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
    openFiles("time.csv", distanceMatrix)


def coordinateMatrix(coordinates: list):
    distanceMatrix = []
    distanceMatrix.append(["City", "latitude", "longitude"])
    cityCount = 0

    city = ['Depot']
    alpha = 'a'
    for i in range(len(coordinates) - 1):
        city.append(alpha)
        alpha = chr(ord(alpha) + 1)

    for i in city:
        distanceMatrix.append(
            [i, coordinates[cityCount][0], coordinates[cityCount][1]])
        cityCount += 1
    # distanceMatrix.append(distanceMatrix[0])
    openFiles("coordinates.csv", distanceMatrix)
    return distanceMatrix, city


def main(coordinates):
    matrix = generateDistanceMatrix(coordinates)
    time_matrix = flight_time(coordinates, 5)
    coordMatrix, city = coordinateMatrix(coordinates)
    print(city)
    return ilp_model(city)


def openFiles(fileName, matrix) -> None:
    """Write csv files

    Args:
        fileName (str): Name of the file
        matrix (list): the 2d array to be written
    """
    with open(fileName, "w") as f:
        writer = csv.writer(f)
        writer.writerows(matrix)


def nn(distanceMatrix: list, nodes: list) -> Tuple[List[int], float]:
    """Nearest Neighbour Path

    Args:
        distanceMatrix (list): Adjancency Matriz
        nodes (list): Contains node ID

    Returns:
        Tuple[List[int], float]: NN Path and it's associated cost 
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


def ilp_model(sites, coordinateFile) -> None:
    """Kara, I., & Bektas, T. (2006). Integer linear programming formulations of multiple salesman problems
        and its variations. European Journal of Operational Research, 174(3), 1449–1458. 
        doi:10.1016/j.ejor.2005.03.008 
    """
    # a handful of sites
    # sites = ['Depot', 'a', 'b', 'c', 'd']

    latlng = ['latitude', 'longitude']
    position = pd.read_csv(coordinateFile, index_col="City")
    flighttime = pd.read_csv('./time.csv', index_col="City")
    distance = pd.read_csv('./distance.csv', index_col="City")
    positions = dict(
        (city, (position.loc[city, 'longitude'], position.loc[city, 'latitude'])) for city in sites)
    distances = dict(((s1, s2), distance.loc[s1, s2])
                     for s1 in positions for s2 in positions if s1 != s2)

    K = 2
    prob = LpProblem("vehicle", LpMinimize)
    # indicator variable if site i is connected to site j in the tour
    # xij as a binary variable equal to 1 if arc (i, j) is in the optimal solution and 0 otherwise
    x = LpVariable.dicts('x', distances, 0, 1, LpBinary)
    # dummy vars to eliminate subtours
    # ui is the number of nodes visited on that travelerÕs path from the origin up to node i (i.e., the visit number of the ith node)
    u = LpVariable.dicts('u', sites, 0, len(sites)-1, LpInteger)
    # the objective (minimize signma c_ij, x_ij)
    cost = lpSum([x[(i, j)]*distances[(i, j)] for (i, j) in distances])
    prob += cost

    # constraints
    for k in sites:
        cap = 1 if k != 'Depot' else K
        # inbound connection
        # we can only enter a node once (Paper pg 2, eq 4), i variable, j contant.
        prob += lpSum([x[(i, k)] for i in sites if (i, k) in x]) == cap
        # outbound connection
        # we can only exit a node once (Paper pg 2 eq 5)
        prob += lpSum([x[(k, i)] for i in sites if (k, i) in x]) == cap

    # subtour elimination
    # generate all combinations of subtour
    N = len(sites)/K
    for i in sites:
        for j in sites:
            if i != j and (i != 'Depot' and j != 'Depot') and (i, j) in x:
                # ui is the number of nodes visited on that travelerÕs path from the origin up to node i (i.e., the visit number of the ith node)
                prob += u[i] - u[j] <= (N)*(1-x[(i, j)]) - 1

    prob.solve()
    print(LpStatus[prob.status])

    non_zero_edges = [e for e in x if value(x[e]) != 0]

    def get_next_site(parent):
        '''helper function to get the next edge'''
        edges = [e for e in non_zero_edges if e[0] == parent]
        for e in edges:
            non_zero_edges.remove(e)
        # 2 edges coming out of depot, K=2
        return edges

    tours = get_next_site('Depot')  # start from the depot
    tours = [[e] for e in tours]  # 2 tours because k = 2

    # tour generate for each drone, because they havent been generated yet
    for t in tours:
        while t[-1][1] != 'Depot':
            t.append(get_next_site(t[-1][1])[-1])

    # the optimal path, debug, remove later
    for t in tours:
        print(' -> '.join([a for a, b in t]+['Depot']))

    totalTime = 0
    for t in tours:
        time = 0
        for i in range(0, len(t)):
            time += flighttime.loc[t[i][0], t[i][1]]
    #         print(flighttime.loc[t[i][0], t[i][1]])
    #     print(time)
        if time > totalTime:
            totalTime = time
    print(totalTime)

    # draw the tours
    # colors = [np.random.rand(3) for i in range(len(tours))]
    # for t, c in zip(tours, colors):
    #     for a, b in t:
    #         p1, p2 = positions[a], positions[b]
    #         plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=c)

    print('Longest time spent:', totalTime, '(min)')
    print('Total distance:', value(prob.objective), '(km)')
    total_distance = value(prob.objective)
    return tours, total_distance, totalTime
