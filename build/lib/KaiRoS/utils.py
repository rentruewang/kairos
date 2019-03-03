import os
import sys
import termios
import tty
from datetime import datetime, timedelta
from os import path

import requests
from requests.exceptions import ConnectionError


def print_help():
    print(
        '''
usage: kairos [h] [n] [f]

optional arguments:
  h, -h, help, --help      
        show this help message and exit

  n, -n, now, --now       
        Displays the current weather

  f, -f, fore, --fore, forecast, --forecast 
        Displays the weather forecast
''')


def handle_connectionerror():
    print("ConnectionError :: please first connect to the Internet!")
    exit()


# adapted from https://github.com/recantha/EduKit3-RC-Keyboard/blob/master/rc_keyboard.py
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def clear_scr():
    os.system('clear')


def println():
    print(flush=True)


def wind_degrees(deg):
    return int((8*(deg+360/16)/360) % 8)


def time_from_now(time):
    from_now = datetime.strptime(time, "%Y-%m-%d %H:%M:%S") - datetime.now()
    days = from_now.days
    hours = from_now.seconds // (60*60)
    minutes = (from_now.seconds % (60*60)) // 60
    seconds = from_now.seconds % 60
    dy = "day" if days <= 1 else "days"
    hr = "hour" if hours <= 1 else "hours"
    mn = "minute" if minutes <= 1 else "minutes"
    sc = "second" if seconds <= 1 else "seconds"
    return "{D} {dy}, {H} {hr}, {M} {mn}, and {S} {sc} from now"\
        .format(D=from_now.days, H=hours, M=minutes, S=seconds, dy=dy, hr=hr, mn=mn, sc=sc)


def from_future(time):
    from_now = datetime.strptime(time, "%Y-%m-%d %H:%M:%S") - datetime.now()
    days = from_now.days
    hours = from_now.seconds // (60*60)
    minutes = (from_now.seconds % (60*60)) // 60
    seconds = from_now.seconds % 60
    return all((days >= 0, hours >= 0, minutes >= 0, seconds >= 0))


def C2F(c):
    return c*(9/5)+32
