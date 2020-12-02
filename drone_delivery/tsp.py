from final import nn, euclideanDist, ilp_model, flight_time, coordinateMatrix,generateDistanceMatrixFinal
from matrix import routeMatrix
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
import sys
sns.set()
pd.options.mode.chained_assignment = None  # default='warn'


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


def k_means():
    """Uses K-Means Clustering Algorithm and returns the centroid of each cluster.
    It also save the coordinates with the cluster label

    Returns:
        [list]: Truck Nodes (Centroids of Clusters)
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

    # elbow ka score. Ideal elbow score at k = 3 (graph's monotonicty / elbow curve)
    print('elbow score -> ', score)
    kmeans = KMeans(n_clusters=3, init='k-means++',
                    max_iter=1000)  # max iteration parameter
    # Compute k-means clustering. # Compute k-means clustering.
    kmeans.fit(X[X.columns[1:3]])

    X['cluster_label'] = kmeans.fit_predict(X[X.columns[1:3]])
    centers = kmeans.cluster_centers_  # Coordinates of cluster centers.

    # Labels of each point (0,0,1,1,2,2)
    labels = kmeans.predict(X[X.columns[1:3]])
    clustered_data = df.merge(X, left_on='City', right_on='City')
    clustered_data = clustered_data.drop(['latitude_y', 'longitude_y'], axis=1)
    clustered_data = clustered_data.rename(
        columns={"latitude_x": 'latitude', "longitude_x": "longitude"})
    centers = kmeans.cluster_centers_
    clustered_data.to_csv('coordinates_kmeans.csv', index=None, header=True)
    # for debugging purposes
    # X.plot.scatter(x='latitude', y='longitude', c=labels, s=50, cmap='viridis')
    # plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    return centers


def kMeansNodes():
    """It gives us the TSP Route of the truck nodes
    Returns:
        list: truck nodes
    """
    centers = k_means()
    # truck rendevouz node for truck in each cluster
    print("Centers  ->", centers)
    nodes = [x for x in range(3)]  # because there are 3 clusters present
    coordinates = centers.tolist()
    distanceMatrix = generateDistanceMatrix(coordinates)
    # generateDistanceMatrix(coordinates)
    print("distanceMatrix -> ", distanceMatrix)
    truck_route_matrix = routeMatrix(centers)
    print('coordinates -> ' , truck_route_matrix)
    tour, cost = nn(truck_route_matrix, nodes)
    return centers, tour, cost


def getCities():
    data = []
    for i in range(3):
        fileName = 'test' + str(i) + '.csv'
        df = pd.read_csv(fileName)
        city = df['City'].to_list()
        print(city)
        tours, tour_distance, tour_time = ilp_model(city, fileName)
        print('----------- ilp done')
        depot = df.iloc[0].to_list()[1:]
        print('tours -> ', tours)
        data.append([tours, tour_distance, tour_time])
    return data


def makeAllSubRoutes(center):
    # initial warehouse is assumed to be far away from the delivery zones. So the truck will travel from the initial warehouse to each zones (clusters)
    # Each path should be in the form - ['Depot', 'a', 'b', 'c', 'd']
    # center = k_means()
    df = pd.read_csv('coordinates_kmeans.csv')
    df = df.sort_values(by=['cluster_label'])
    # df = df.drop(columns = ['cluster_label'])
    # print(df.head(100))
    # center = [[28.63533523, 77.21035865], [
    # 28.63621989, 77.2259356], [28.63078809, 77.24152565]]
    final = []
    for i in center:
        temp = ["Depot"]
        for coord in i:
            temp.append(coord)
        final.append(temp)
    # final is the row
    # print(final)
    arr = df.to_numpy()
    clusters = [x for x in range(3)]
    sub_regions = []
    for x in clusters:
        sub_region = [["City", "latitude", "longitude"], final[x]]
        for row in arr:
            if row[-1] == x:
                first_3_only = row[0: len(row) - 1]
                sub_region.append(first_3_only)
        sub_regions.append(sub_region)
    # print(sub_regions[1])

    cnt = 0
    for cluster in sub_regions:
        df2 = pd.DataFrame(cluster[1:], columns=cluster[0])
        # print(df2.head(100))
        df2.to_csv('test' + str(cnt) + '.csv',  index=None, header=True)
        cnt += 1
    # pass these coordinate matrices to the main() in final.py


def main(coordinates):
    generateDistanceMatrixFinal(coordinates)
    flight_time(coordinates, 5)
    coordMatrix, city = coordinateMatrix(coordinates)
    centers, tsp_route, tsp_cost = kMeansNodes()
    print("truck tour -> ", tsp_route, " tsp_cost -> ",
          tsp_cost, 'centers -> ', centers)
    makeAllSubRoutes(centers)
    data = getCities()
    print('debug -> \n',data)
    return data, centers, tsp_route
