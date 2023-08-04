from buoy.station import Station


class BuoyData:
    def __init__(self, id: str):
        self.data_path = 'https://www.ndbc.noaa.gov/data/'
        self.id = id
        self.station = Station(self.id)
        