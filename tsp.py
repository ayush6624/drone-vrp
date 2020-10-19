import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
import sys
sns.set()


# clustered_data = df.merge(X, left_on='parcelid', right_on='parcelid')
# clustered_data.head(5)
# City,latitude,longitude

def k_means():
    """Return centroid of each cluster ,and also save the coordinates with the cluster label

    Returns:
        [type]: [description]
    """
    df = pd.read_csv('coordinates.csv')
    X = df[1:]  # removed the depot
    # print(X.head(10))
    K_clusters = range(1, 10)  # exp b/w 1 and 10 clustrers
    # we generate model for each "k" clusters
    kmeans = [KMeans(n_clusters=i) for i in K_clusters]
    Y_axis = df[['latitude']]
    X_axis = df[['longitude']]
    score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]

    #  print(score) # elbow ka score. Ideal elbow score at k = 3 (graph's monotonicty / elbow curve)
    kmeans = KMeans(n_clusters=3, init='k-means++')
    # Compute k-means clustering. # Compute k-means clustering.
    kmeans.fit(X[X.columns[1:3]])

    X['cluster_label'] = kmeans.fit_predict(X[X.columns[1:3]])d
    centers = kmeans.cluster_centers_  # Coordinates of cluster centers.

    # Labels of each point (0,0,1,1,2,2)
    labels = kmeans.predict(X[X.columns[1:3]])
    print(X.head(10))
    centers = kmeans.cluster_centers_
    X.to_csv('coordinates_kmeans.csv')
    # for debugging purposes
    # X.plot.scatter(x='latitude', y='longitude', c=labels, s=50, cmap='viridis')
    # plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    return centers


c = k_means()
nodes = [x for x in range(3)]
print(nodes)

coordinates =c.tolist()
print(coordinates)
from final import euclideanDist

def generateDistanceMatrix(coordinates: list):
    """Generate Adjacency Matrix

    Args:
        coordinates (list): coordinates

    Returns:
        matrix: 2D lists
    """
    distanceMatrix = []
    for i in range(len(coordinates)):
        matrix = []
        # matrix.append(city[cityCount])
        for j in range(len(coordinates)):
            if i == j:
                matrix.append(0)
            else:
                matrix.append(euclideanDist(i, j, coordinates))
        distanceMatrix.append(matrix)
    return distanceMatrix

distanceMatrix = generateDistanceMatrix(coordinates)
print(generateDistanceMatrix(coordinates))

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
    # return nnTour, nnCost
    return nnTour


tour = nn(distanceMatrix, nodes)
print(tour)