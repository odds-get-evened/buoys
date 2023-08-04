import re
from enum import Enum
from urllib.request import urlopen, Request

from buoy.data import BuoyData


class BuoyHourly(BuoyData):
    def __init__(self, id: str, start_hour: int = 0, end_hour: int = 23):
        super().__init__(id)

        self.observations = []
        self.files = []
        self.data = []

        self.id = id

        self.hour_from = start_hour
        self.hour_to = end_hour

        self.set_time_ranges()

        self.set_files()

        self.set_data()

        self.set_observations()

    def set_data(self):
        for i, url in enumerate(self.files):
            with urlopen(url, None, 30) as u:
                content: str = u.read().decode('utf8').strip()
                lines = re.split(r"[\r\n]+", content)
                
                for line in lines:
                    if not line.startswith('#') and line != "":  # skip, empty, header, and comment lines
                        stn_id = line[0:7]
                        '''
                        if station ID has a space in it, it's invalid
                        we've the string end into the next column, and this means
                        IDs are allotted 7 characters from the old 5
                        '''
                        if ' ' in stn_id:
                            stn_id = line[0:5]

                        if stn_id == self.id:
                            # only get rows that include this station's ID
                            # line = line.replace_all(r" +", "|", 19)
                            line = re.sub(r"\s+", '|', line)
                            obs = line.split('|')
                            self.data.append(obs)



    def get_data(self):
        pass

    def set_time_ranges(self):
        if self.hour_from >= self.hour_to:
            print("start time must be less than and not equal to end time.")
            exit(-1)
        else:
            '''
            current hour is not recorded/posted yet
            so we offset both hours by one
            '''
            self.hour_from = (self.hour_from - 1)
            self.hour_to = (self.hour_to - 1)

    def set_files(self):
        [
            self.files.append(self.data_path + 'hourly2/hour_' + "%02d" % i + '.txt')
            for i in range(self.hour_from, self.hour_to)
        ]

    def set_observations(self):
        [self.observations.append(self.observation(i)) for i in self.data]

    def observation(self, d):
        pass


class ObservationFieldMap(Enum):
    id = 0
    year = 1
    month = 2
    day = 3
    hour = 4
    min = 5
    timestamp = 6
    wind_direction = 7
    wind_speed = 8
    gusts = 9
    wave_height = 10
    dominant_wave_period = 11
    avg_wave_period = 12
    mean_wave_direction = 13
    barometer = 14
    air_temp = 15
    water_temp = 16
    dewpoint = 17
    visibility = 18
    pressure_tendency = 19
    tide = 20
