from buoy.hourly import BuoyHourly


def boot_up():
    bh = BuoyHourly('44018', 9, 12)
    bh.get_data()


boot_up()
