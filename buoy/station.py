import datetime
import json
import os.path
import re
import time
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen

from tinydb import TinyDB

from buoy import constants

STATIONS_TBL_URL = 'https://www.ndbc.noaa.gov/data/stations/station_table.txt'

STN_DB_FILE = Path(os.path.expanduser('~'), '.buoys', 'stations.json')
STN_DB = TinyDB(STN_DB_FILE)

LOCAL_STATIONS_TXT = Path(os.path.expanduser('~'), '.buoys', 'stations_table.txt')


def correction(r):
    key = r[0]
    val = r[1]

    if key == 'location':
        loc_s = val.strip()
        rx = re.findall(r"(\d+\.\d{3,})\s+([NESW])", loc_s)

        # tuple of location field [[lat, direction], [lng, direction]]
        lat = rx[0][0]
        lng = rx[1][0]
        lat_dir = rx[0][1]
        lng_dir = rx[1][1]
        lat = str("-" if lat_dir == 'S' else '') + lat
        lng = str("-" if lng_dir == 'E' else '') + lng
        coords = (float(lat), float(lng))

        return key, coords  # return modified location tuple
    else:
        return r  # return all other tuple sets


def save_station(items):
    d = []

    [d.append((constants.StationFieldMap(i).name, v)) for i, v in enumerate(items)]

    # normalize lat/long (location)
    d = [correction(j) for j in d]

    j = dict(d)
    # j_str = json.dumps(j)

    STN_DB.insert(j)


def sync_station_data(path):
    if not path.exists():
        station_sync()

    if not STN_DB_FILE.exists():
        STN_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        STN_DB_FILE.touch()

    STN_DB.truncate()

    with path.open('r') as f:
        [save_station(line.split('|')) for line in f.readlines() if not line.startswith('#')]


def station_sync(force=False):
    if not LOCAL_STATIONS_TXT.exists():
        LOCAL_STATIONS_TXT.parent.mkdir(parents=True, exist_ok=True)
        LOCAL_STATIONS_TXT.touch()

    ''' compare local mod time to now '''
    diff = time.time() - os.path.getmtime(LOCAL_STATIONS_TXT)
    hours = round((diff / (1000 * 60 * 60)) % 24)
    now = datetime.datetime.now()
    mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(LOCAL_STATIONS_TXT))
    days_delta = (now - mod_time).days

    if days_delta > 1 or force is True:  # over 24 hours is old, so update...
        print("updating local stations data (" + LOCAL_STATIONS_TXT.name + ").")
        with urlopen(STATIONS_TBL_URL, None, 30) as remote:
            remote_data = remote.read()

        with LOCAL_STATIONS_TXT.open('r') as local:
            local_data = local.read()
            local.close()

        local_hash = sha256(local_data.encode()).hexdigest()
        remote_hash = sha256(remote_data).hexdigest()
        if local_hash != remote_hash:
            # out of sync, so update local file from remote one.
            with LOCAL_STATIONS_TXT.open('w') as lf:
                lf.write(remote_data.decode())
                lf.close()

        print("updated stations table data. saved to " + LOCAL_STATIONS_TXT.name)
        sync_station_data(LOCAL_STATIONS_TXT)


class Station:
    def __init__(self, id: str):
        self.id = id
        self.owner_id = None
        self.ttype = None
        self.hull = None
        self.name = None
        self.payload = None
        self.location = None
        self.note = None
