from enum import Enum

NBDC_ROOT_URL = 'https://www.ndbc.noaa.gov/data/'


class ObservationFieldMap(Enum):
    id = 0
    year = 1
    month = 2
    day = 3
    hour = 4
    min = 5
    wind_direction = 6
    wind_speed = 7
    gusts = 8
    wave_height = 9
    dominant_wave_period = 10
    avg_wave_period = 11
    mean_wave_direction = 12
    barometer = 13
    air_temp = 14
    water_temp = 15
    dewpoint = 16
    visibility = 17
    pressure_tendency = 18
    tide = 19


class StationFieldMap(Enum):
    id = 0
    owner = 1
    ttype = 2
    hull = 3
    name = 4
    payload = 5
    location = 6
    timezone = 7
    forcast = 8
    note = 9
