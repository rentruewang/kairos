import os
from datetime import datetime
from os import path
from socket import gaierror
from sys import stdout

from requests.exceptions import ConnectionError
from termcolor import cprint

from .reference import (ASCII_ART, COLOR, END, LOOKUP_ICON, LOOKUP_WIND, NAME,
                        WARNING_COLOR, ZERO)
from .utils import (C2F, clear_scr, from_future, getch, handle_connectionerror,
                    time_from_now, wind_degrees)
from .weather import Forecast, Weather


class TerminalInterface:
    def __init__(self):
        pass

    def info(self):
        cprint(ASCII_ART, color=COLOR)

    def weather(self, loc=None):
        w = Weather(loc=loc)
        try:
            wttr = w.here.get.weather
            self.display_weather_info(wttr)
        except ConnectionError:
            handle_connectionerror()

    def display_weather_info(self, wttr):
        print("It's {}".format(str(datetime.now()).split('.')[0]))
        try:
            icon = LOOKUP_ICON[wttr["weather"][0]["icon"][:2]]
            temp_C = wttr["main"]["temp"]-ZERO
            cprint("{temp:.1f}".format(temp=temp_C),
                   end='', color=COLOR, flush=True)
            print("°C/", end='', flush=True)
            cprint("{tempF:.1f}".format(tempF=C2F(temp_C)),
                   end='', color=COLOR, flush=True)
            print("°F  {icon}".format(
                icon=icon), end=END)
        except KeyError:
            pass
        print(wttr["weather"][0]["main"], end=END)
        print(wttr["weather"][0]["description"], end=END)
        print("in {country} {loc}".format(
            country=wttr["sys"]["country"],
            loc=(wttr["coord"]["lon"], wttr["coord"]["lat"])), end='')
        print()
        drc = wind_degrees(wttr["wind"]["deg"])
        print("Wind: {deg}  {speed}(m/s)".format(
            deg=LOOKUP_WIND[drc], speed=wttr["wind"]["speed"]), end='')
        print()

    def forecast(self, loc=None):
        f = Forecast(loc=loc)
        try:
            fore = f.here.get.forecast
            self.display_forecast_info(fore)
        except ConnectionError:
            handle_connectionerror()

    def display_forecast_info(self, full_forecast):
        index = 0
        try:
            while not from_future(full_forecast["list"][index]["dt_txt"]):
                index += 1
        except IndexError:
            cprint("No up-to-date data available :(",
                   color=WARNING_COLOR, flush=True)
            return
        start_index = index
        show_entry = True
        while True:
            if show_entry:
                self.print_entry(fore=full_forecast["list"][index],
                                 city=full_forecast["city"])

            cprint("Input", end='', color=COLOR, flush=True)
            print(": [", end='', flush=True)
            cprint("f", end='', color=COLOR, flush=True)
            print("]orward 3 hours, [", end='', flush=True)
            cprint("b", end='', color=COLOR, flush=True)
            print("]ackward 3 hours, [", end='', flush=True)
            cprint("q", end='', color=COLOR, flush=True)
            print("]uit: ", end='', flush=True)
            typed = getch().lower()

            if typed == 'b':
                if index == start_index:
                    cprint("No more entries!\a", end='', color=WARNING_COLOR)
                    print()
                    show_entry = False
                    continue
                index -= 1
                show_entry = True
            elif typed == 'f':
                if index == full_forecast["cnt"] - 1:
                    cprint("No more entries!\a", end='', color=WARNING_COLOR)
                    print()
                    show_entry = False
                    continue
                index += 1
                show_entry = True
            elif typed == 'q' or typed == "quit":
                print(flush=True)
                break
            else:
                cprint('Invalid input\a', end='', color=WARNING_COLOR)
                show_entry = False
                print()
                continue

            clear_scr()

    def print_entry(self, fore, city):
        print("Forecast: {time}{END}{from_now}".format(
            END=END,
            time=fore["dt_txt"],
            from_now=time_from_now(fore["dt_txt"])), end='')
        print()
        try:
            i = fore["weather"][0]["icon"][:2]
            icon = LOOKUP_ICON[i]
            temp_C = fore["main"]["temp"]-ZERO
            cprint("{temp:.1f}".format(temp=temp_C),
                   end='', color=COLOR, flush=True)
            print("°C/", end='', flush=True)
            cprint("{tempF:.1f}".format(tempF=C2F(temp_C)),
                   end='', color=COLOR, flush=True)
            print("°F  {icon}".format(
                icon=icon, temp=temp_C, tempF=C2F(temp_C)), end=END)
        except KeyError:
            pass
        print("{main}".format(main=fore["weather"][0]["main"]), end=END)
        print("{description}".format(
            description=fore["weather"][0]["description"]), end=END)
        print("in {country} ({lon:.1f},{lat:.1f})".format(country=city["country"],
                                                          lon=city["coord"]["lon"], lat=city["coord"]["lat"]), end='')
        print()

        drc = wind_degrees(fore["wind"]["deg"])
        print("Wind: {wind}  {speed}(m/s)".format(wind=LOOKUP_WIND[drc],
                                                  speed=fore["wind"]["speed"]), end='')
        print()
