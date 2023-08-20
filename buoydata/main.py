import json
import re
import sys
import threading

from buoy.constants import StationFieldMap
from buoy.hourly import BuoyHourly
from buoy.station import station_sync, STN_DB, LOCAL_STATIONS_TXT
from buoy.ui.window import BuoyWindow
from geoquery.geode import get_lat_long


def hourly_cmd(args: list[str]):
    try:
        _id = args[0].strip()
        start = int(args[1].strip())
        end = int(args[2].strip())

        bh = BuoyHourly(_id, start, end)
        print(json.dumps(bh.get_observations(), sort_keys=False, indent=4))
    except ValueError:
        print('start and end hours must be integer values. value error.')
        exit(-1)
    except IndexError as e:
        print('please provide station ID and start and end hours')
        exit(-1)


def station_cmd(args: list[str]):
    """
    all the console commands for buoys application
    :param args: tuple of args from system
    """
    try:
        task = args[0].strip()

        if task == 'find':
            try:
                q = " ".join(args[1:])
                coords = get_lat_long(q)
                print(coords)
            except IndexError as ie:
                print('find task requires a location query')
                exit(-1)

        if task == 'sync':
            station_sync(force=True)
            print("station data sync has completed.")

        if task == 'list':
            print("%s%40s" % ('ID', 'name (partial)'))
            [print("%s%40s" % (stn[StationFieldMap.id.name], stn[StationFieldMap.name.name][0:35])) for stn in STN_DB.all()]

    except IndexError:
        print('please provide a task (e.g. `find`, `list`)')
        exit(-1)


def open_gui():
    BuoyWindow()


def do_cmd(args: list[str]):
    if len(args) == 0:
        print("please choose a command (hourly, station)")
        exit(-1)

    the_cmd = args[0]
    the_rest = args[1:]

    match the_cmd:
        case 'hourly':  # needs station ID, start, and end
            hourly_cmd(the_rest)
        case 'station':
            station_cmd(the_rest)
        case 'gui':
            open_gui()
        case _:
            print('not a valid command')
            exit(-1)


def boot_up():
    # sync station list from remote URL
    stn_sync_t = threading.Thread(target=station_sync)
    stn_sync_t.run()

    # run main program
    a = sys.argv[1:]
    do_cmd(a)
