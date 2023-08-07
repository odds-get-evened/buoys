import sys
from buoy.hourly import BuoyHourly
from buoy.station import station_sync


def hourly_cmd(args):
    try:
        id = args[0].strip()
        start = int(args[1].strip())
        end = int(args[2].strip())

        bh = BuoyHourly(id, start, end)
        print(bh.get_observations())
    except ValueError as e:
        print('start and end hours must be integer values')
        exit(-1)
    except TypeError as e:
        print('start and end hours must be integer values')
        exit(-1)
    except IndexError as e:
        print('please provide station ID and start and end hours')
        exit(-1)


def station_cmd(the_rest):
    pass


def do_cmd(args):
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
    station_sync()
    # run main program
    args = sys.argv[1:]
    do_cmd(args)
