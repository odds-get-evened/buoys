import json
import math
from urllib import request
from urllib.parse import urlunsplit, urlencode


def get_lat_long(street_address: str) -> tuple:
    """gets a latitude/longitude pair from street address

    Parameters:
        street_address (str): address query

    Returns:
        tuple: a coordinate.

    """
    qry = urlencode(dict(
        format="json", addressdetails=1, polygon=1,
        q=street_address.strip()
    ))

    url = urlunsplit((
        'https', 'nominatim.openstreetmap.org', 'search',
        qry, ""
    ))

    with request.urlopen(url) as res:
        data = json.loads(res.read())
        # print(json.dumps(data, indent=4, sort_keys=True))
        return data[0]['lat'], data[0]['lon']


def get_grid(lat, long):
    url = urlunsplit((
        'https', 'api.weather.gov',
        'points' + '/' + lat + "," + long, None, None
    ))

    with request.urlopen(url) as res:
        data = json.loads(res.read())
        # print(json.dumps(data, indent=4, sort_keys=True))
        return (
            data['properties']['gridId'],
            data['properties']['gridX'],
            data['properties']['gridY'],
            data['properties']['observationStations']  # a fucking URL
        )


def get_forecast(grid):
    url = urlunsplit((
        'https', 'api.weather.gov',
        "gridpoints/" + str(grid[0]) + "/" + str(grid[1]) + "," + str(grid[2]) + "/forecast",
        None, None
    ))

    with request.urlopen(url) as res:
        data = json.loads(res.read())
        return data['properties']['periods']


def get_stations(grid):
    with request.urlopen(grid[3]) as res:
        data = json.loads(res.read())
        return data['features']


def get_observation(station_id):
    url = urlunsplit((
        'https', 'api.weather.gov',
        'stations/' + station_id + '/observations',
        None, None
    ))

    with request.urlopen(url) as res:
        data = json.loads(res.read())

        return data['features']


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # earth's radius in km.

    # convert degrees to radians
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # distance


def get_nearby_coordinates(center_lat, center_lon, radius):
    """gets nearby coordinates within a radius in kilometers

    Parameters:
        center_lat (double): center latitude
        center_lon (double): center longitude
        radius (int): radius in kilometers

    Returns:
        list: a list of coordinate tuples (lat, lon)

    """

    nearby_coords = []

    for lat in range(-90, 91, 1):
        for lon in range(-180, 181, 1):
            distance = haversine(center_lat, center_lon, lat, lon)

            if distance <= radius:
                nearby_coords.append((lat, lon))

    return nearby_coords
