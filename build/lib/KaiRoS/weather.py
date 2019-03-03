import json

import requests

from .reference import API_KEY, FORECAST, IP_INFO, WEATHER


class Location:
    def __init__(self):
        pass

    @property
    def get(self):
        # ignores exceptions by design
        r = requests.get(IP_INFO)
        r = json.loads(r.text)

        self.region = r["region"]
        self.city = r["city"]
        self.country = r["country"]
        self.location = tuple(float(f) for f in r["loc"].split(','))

        return self


class Weather:
    def __init__(self, loc=None):
        self.location = Location()
        self.loc = loc

    @property
    def get(self):
        lat, lon = self.loc if self.loc else \
            tuple(int(i) for i in self.location.get.location)

        r = requests.get(url=WEATHER.format(lat=lat, lon=lon, api=API_KEY))
        self.weather = json.loads(r.text)
        return self

    @property
    def here(self):
        self.location.get
        return self


class Forecast:
    def __init__(self, loc=None):
        self.location = Location()
        self.loc = loc

    @property
    def get(self):
        lat, lon = self.loc if self.loc else \
            tuple(int(i) for i in self.location.get.location)

        r = requests.get(url=FORECAST.format(lat=lat, lon=lon, api=API_KEY))
        self.forecast = json.loads(r.text)
        return self

    @property
    def here(self):
        self.location.get
        return self
