import json
import os.path
from itertools import chain
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from tinydb import Query

from buoy.constants import StationFieldMap as stn_map, ObservationFieldMap as obs_map
from buoy.hourly import BuoyHourly
from buoy.station import STN_DB


def test_cache(id, start, end, update_cache=False) -> list[dict]:
    cache_file = Path(os.path.expanduser('~'), '.buoys', 'cache.json')
    if not cache_file.exists():
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.touch()

    if update_cache is True:
        buoy_data = BuoyHourly(id, start, end)
        with cache_file.open('w') as fh:
            temp = []
            [temp.append(x) for x in buoy_data.get_observations()]
            temp = [y for y in temp]

            j = json.dumps(temp)
            fh.write(j)
            del j
            del temp
            fh.close()

    with cache_file.open('r') as fh:
        c = fh.read()
        j = json.loads(c)
        fh.close()
        return j


def append_station(obs: dict) -> dict:
    stn = Query()
    r = STN_DB.search(stn.id == obs['id'])[0]
    obs.update({'station': r})

    return obs


def normalize_obs(obs):
    o = {
        stn_map.location.name: obs['station'][stn_map.location.name],
        obs_map.wind_direction.name: obs[obs_map.wind_direction.name],
        obs_map.wind_speed.name: obs[obs_map.wind_speed.name],
        obs_map.gusts.name: obs[obs_map.gusts.name],
        obs_map.wave_height.name: obs[obs_map.wave_height.name],
        obs_map.dominant_wave_period.name: obs[obs_map.dominant_wave_period.name],
        obs_map.avg_wave_period.name: obs[obs_map.avg_wave_period.name],
        obs_map.mean_wave_direction.name: obs[obs_map.mean_wave_direction.name],
        obs_map.barometer.name: obs[obs_map.barometer.name],
        obs_map.air_temp.name: obs[obs_map.air_temp.name],
        obs_map.water_temp.name: obs[obs_map.water_temp.name],
        obs_map.dewpoint.name: obs[obs_map.dewpoint.name],
        obs_map.visibility.name: obs[obs_map.visibility.name],
        obs_map.pressure_tendency.name: obs[obs_map.pressure_tendency.name],
        obs_map.tide.name: obs[obs_map.tide.name],
        'timestamp': obs['timestamp']
    }

    o = {k: v if v != '' else None for k, v in o.items()}

    return o


def obs_line_chart(obs):
    print(json.dumps(obs, indent=4))


def main():
    obs = test_cache('41115', 0, 12)
    obs = [append_station(x) for x in obs]

    normed_obs = [normalize_obs(x) for x in obs]

    obs_line_chart(normed_obs)


if __name__ == "__main__":
    main()
