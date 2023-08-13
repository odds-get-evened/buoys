import json
import sys
import threading

from buoy.hourly import BuoyHourly
from buoy.station import station_sync


def hourly_cmd(args):
    try:
        id = args[0].strip()
        start = int(args[1].strip())
        end = int(args[2].strip())

        bh = BuoyHourly(id, start, end)
        print(json.dumps(bh.get_observations(), sort_keys=True, indent=4))
    except ValueError as e:
        print('start and end hours must be integer values')
        exit(-1)
    except TypeError as e:
        print('start and end hours must be integer values')
        exit(-1)
    except IndexError as e:
        print('please provide station ID and start and end hours')
        exit(-1)


def station_cmd(args):
    try:
        task = args[0].strip()
        print(task)

        if task == 'find':
            try:
                q = " ".join(args[1:])
                print(q)
            except IndexError as ie:
                print('find task requires a location query')
                exit(-1)

            print(q)
    except IndexError as ie:
        print('please provide a task (e.g. `find`)')
        exit(-1)

def do_cmd(args):
    station_sync()  # grab new station list from remote text file

    if len(args) == 0:
        print("please choose a command")
        exit(-1)

    the_cmd = args[0]
    the_rest = args[1:]

    match the_cmd:
        case 'hourly':  # needs station ID, start, and end
            hourly_cmd(the_rest)
        case 'station':
            station_cmd(the_rest)
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
