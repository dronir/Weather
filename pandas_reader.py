import pandas as pd
from datetime import datetime
from numpy import nan as NaN
from sys import argv
from os import path


BOLTWOOD_COLUMNS = [
    "day", "month", "year", "hour", "minute", "second",
    "clouds", "wind", "rain", "daylight",
    "skyTemp", "ambientTemp", "sensorTemp",
    "windSpeed",
    "humidity", "dewPoint",
    "dayLightValue",
    "rainDrop", "sensorWet",
    "heaterPower",
    "windUnits",
]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
BOLTWOOD_CLOUD_VALUE = ["unknown", "clear", "cloudy", "very cloudy"]
BOLTWOOD_WIND_VALUE = ["unknown", "calm", "windy", "very windy"]
BOLTWOOD_RAIN_VALUE = ["unknown", "dry", "wet", "rain"]
BOLTWOOD_DAYLIGHT_VALUE = ["unknown", "dark", "light", "very light"]

# A bunch of functions to convert column values in Boltwood data
BOLTWOOD_CONVERTERS = {
    "clouds" : lambda i: BOLTWOOD_CLOUD_VALUE[int(i)],
    "rain" : lambda i: BOLTWOOD_RAIN_VALUE[int(i)],
    "wind" : lambda i: BOLTWOOD_WIND_VALUE[int(i)],
    "daylight" : lambda i: BOLTWOOD_DAYLIGHT_VALUE[int(i)],
    "month" : lambda i: MONTHS[int(i)-1],
    "year" : int,
    "day" : int,
    "hour" : int,
    "minute" : int,
    "second" : int
}

NUUKSIO_CONVERTERS = {
    "cloudCover" : float
}

VAISALA_CONVERTERS = {
    "data" : lambda s: NaN if "/" in s else float(s)
}

def read_boltwood(filename):
    """Read Boltwood data file and return a Pandas DataFrame.
    The column names defined above are used, and the indexing is by the timestamp."""
    data = pd.read_table(filename, delim_whitespace=True, index_col=0,
                         parse_dates={"timestamp":[0,1,2,3,4,5]}, keep_date_col=True,
                         names=BOLTWOOD_COLUMNS, converters=BOLTWOOD_CONVERTERS,
                         infer_datetime_format=True)
    # This is slow and crude, but can't of a better way to do it now:
    dates = [datetime.strptime(x, "%d %b %Y %H %M %S") for x in data.index]
    return data.set_index(pd.DatetimeIndex(dates))


def read_clouds(filename):
    return pd.read_table(filename, delim_whitespace=True, index_col=0,
                         parse_dates={"timestamp":[0]}, names=["foo", "cloudCover"],
                         converters=NUUKSIO_CONVERTERS)


def convert_datetime(dates, times):
    N = len(dates)
    output = []
    for i in range(N):
        line = "{} {}".format(dates[i], times[i])
        output.append(pd.to_datetime(line, format="%d.%m.%Y %H:%M:%S"))
    return output

form = "%d.%m.%Y %H:%M:%S"

def read_vaisala(filename):
    data = pd.read_table(filename, delim_whitespace=True, names=["date", "time", "value"],
                         encoding="utf-8-sig", na_values="///", parse_dates=[[0,1]],
                         index_col=0, converters=VAISALA_CONVERTERS,
                         date_parser=convert_datetime)
    return data

def pickle_vaisala(filename):
    data = read_vaisala(filename)
    data.to_pickle("pickled_vaisala.dat")

if __name__=="__main__":
    data = read_boltwood(argv[1])
    data.to_pickle("pickled_{}.dat".format(path.basename(argv[1])))
