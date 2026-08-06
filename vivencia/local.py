#Aprovar Localozação.
from math import radians, sin, cos, sqrt, atan2


def calcular_distancia(lat1, lon1, lat2, lon2):

    R = 6371000  # raio da Terra em metros

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))

    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia = R * c

    return distancia