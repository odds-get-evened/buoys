import sys

from buoy.hourly import BuoyHourly


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


def do_cmd(args):
    if len(args) == 0:
        print("please choose a command")
        exit(-1)

    the_cmd = args[0]
    the_rest = args[1:]

    match the_cmd:
        case 'hourly':  # needs station ID, start, and end
            hourly_cmd(the_rest)
        case _:
            print('not a valid command')
            exit(-1)


def boot_up():
    args = sys.argv[1:]
    do_cmd(args)

    # bh = BuoyHourly('44018', 9, 12)
    # print(bh.get_observations())
