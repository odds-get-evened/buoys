import datetime
import re
import zoneinfo
from urllib.request import urlopen

from buoy import constants
from buoy.constants import ObservationFieldMap


class BuoyHourly:
    def __init__(self, sid: str, start_hour: int = 0, end_hour: int = 23):
        self.observations = []
        self.files = []
        self.data = []

        self.id = sid

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
                            line = re.sub(r"\s+", '|', line, 20)
                            obs = line.split('|')
                            self.data.append(obs)

    def get_observations(self):
        return self.observations

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
            self.files.append(constants.NBDC_ROOT_URL + 'hourly2/hour_' + "%02d" % i + '.txt')
            for i in range(self.hour_from, self.hour_to)
        ]

    def set_observations(self):
        [self.observations.append(self.observation(i)) for i in self.data]

    '''
    map each row's list of column's values to a dictionary
    that is modeled after the text's schema
    more details: https://www.ndbc.noaa.gov/faq/measdes.shtml
    '''

    def observation(self, d: list):
        obs_data = []
        [obs_data.append((ObservationFieldMap(i).name, v)) for i, v in enumerate(d)]

        obs_data = [self.corrections(j) for j in obs_data]

        # roll up dates and times into one datetime field
        dt = datetime.datetime(
            obs_data[ObservationFieldMap.year.value][1],
            obs_data[ObservationFieldMap.month.value][1],
            obs_data[ObservationFieldMap.day.value][1],
            hour=obs_data[ObservationFieldMap.hour.value][1],
            minute=obs_data[ObservationFieldMap.min.value][1]
        ).astimezone(datetime.timezone.utc).timestamp()
        obs_data.append(('timestamp', dt))

        od = dict(obs_data)

        # remove all the time fields from dict
        od.pop(ObservationFieldMap.year.name)
        od.pop(ObservationFieldMap.month.name)
        od.pop(ObservationFieldMap.day.name)
        od.pop(ObservationFieldMap.hour.name)
        od.pop(ObservationFieldMap.min.name)

        return od

    def corrections(self, obs: tuple) -> tuple:
        """
        since all values are returned as strings this gets all data
        into appropriate types
        :param obs:
        :return:
        """
        key = obs[0]
        val = obs[1]

        dont_touch = ['id']

        # let's convert all numeric strings to integers
        if key not in dont_touch:
            if val.isdigit():
                val = int(val)
            else:
                # convert decimal values to floats
                try:
                    float(val)
                    val = float(val)
                except ValueError as e:
                    pass

        try:
            if val.lower() == 'mm':
                val = ''
        except AttributeError as e:
            pass

        return key, val
