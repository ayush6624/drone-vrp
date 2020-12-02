import requests
import os


def routeMatrix(coordinates):
    distance_matrix = []
    key = os.environ['GOOGLE_MAPS_API']
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins='
    for c in coordinates:
        url = url + str(c[0]) + ',' + str(c[1]) + '%7C'

    url = url[:-3]

    url += '&destinations='

    for c in coordinates:
        url = url + str(c[0]) + ','+str(c[1]) + '%7C'

    url = url[:-3]

    url = url + "&key=" + key

    r = requests.get(url)
    resp = r.json()
    for i in resp['rows']:
        row = []
        for j in i['elements']:
            row.append(j['distance']['value'])
        distance_matrix.append(row)

    return distance_matrix
