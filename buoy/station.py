import json
import os.path
import threading
import time
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen

from tinydb import TinyDB
from tinydb.table import Document

from buoy import constants

STATIONS_TBL_URL = 'https://www.ndbc.noaa.gov/data/stations/station_table.txt'

DB_FILE = Path(os.path.expanduser('~'), '.buoys', 'stations.json')
DB = TinyDB(DB_FILE)


def save_station(items):
    d = []

    [d.append((constants.StationFieldMap(i).name, v)) for i, v in enumerate(items)]

    j = dict(d)
    j_str = json.dumps(j)

    DB.insert(j)


def sync_station_data(path):
    if not path.exists():
        station_sync()

    if not DB_FILE.exists():
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        DB_FILE.touch()

    DB.truncate()

    with path.open('r') as f:
        [save_station(line.split('|')) for line in f.readlines() if not line.startswith('#')]


def station_sync():
    local_file = Path(os.path.expanduser('~'), '.buoys', 'stations_table.txt')

    diff = time.time() - os.path.getmtime(local_file)
    hours = round((diff / (1000 * 60 * 60)) % 24)

    if not local_file.exists():
        local_file.parent.mkdir(parents=True, exist_ok=True)
        local_file.touch()

    if hours > 23:  # over 24 hours is old, so update...
        print("updating local stations data (" + local_file.name + ").")
        with urlopen(STATIONS_TBL_URL, None, 30) as remote:
            remote_data = remote.read()

        with local_file.open('r') as local:
            local_data = local.read()
            local.close()

        local_hash = sha256(local_data.encode()).hexdigest()
        remote_hash = sha256(remote_data).hexdigest()
        if local_hash != remote_hash:
            # out of sync, so update local file from remote one.
            with local_file.open('w') as lf:
                lf.write(remote_data.decode())
                lf.close()

        print("updated stations table data. saved to " + local_file.name)
        sync_station_data(local_file)



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
