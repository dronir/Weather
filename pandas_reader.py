import pandas as pd
from sys import argv

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
    "month" : lambda i: MONTHS[int(i)-1]
}

def read_boltwood(filename):
    """Read Boltwood data file and return a Pandas DataFrame.
    The column names defined above are used, and the indexing is by the timestamp."""
    return pd.read_table(filename, delim_whitespace=True, index_col=0,
                         parse_dates={"timestamp":[2,1,0,3,4,5]}, keep_date_col=True,
                         names=BOLTWOOD_COLUMNS, converters=BOLTWOOD_CONVERTERS)

if __name__=="__main__":
    print(read_boltwood(argv[1]))
