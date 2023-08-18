import json
import sys
import threading

from buoy.hourly import BuoyHourly
from buoy.station import station_sync, STN_DB
from buoy.ui.window import BuoyWindow
from geoquery.geode import get_lat_long


def hourly_cmd(args: list[str]):
    try:
        id = args[0].strip()
        start = int(args[1].strip())
        end = int(args[2].strip())

        bh = BuoyHourly(id, start, end)
        print(json.dumps(bh.get_observations(), sort_keys=False, indent=4))
    except ValueError as e:
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
        print(task)

        if task == 'find':
            try:
                q = " ".join(args[1:])
                coords = get_lat_long(q)
                print(coords)
            except IndexError as ie:
                print('find task requires a location query')
                exit(-1)

        if task == 'list':
            print("%10s%64s" % ('id', 'name'))
            [print("%10s%64s" % (i['id'], i['name'])) for i in STN_DB.all()]
    except IndexError as ie:
        print('please provide a task (e.g. `find`)')
        exit(-1)


def open_gui():
    BuoyWindow()


def do_cmd(args: list[str]):
    station_sync()  # grab new station list from remote text file

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
