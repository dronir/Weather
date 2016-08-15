import pandas as pd
import numpy as np
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

def read_boltwood(filename):
    """Read Boltwood data file and return a Pandas DataFrame.
    The column names defined above are used, and the indexing is by the timestamp."""
    return pd.read_table(filename, delim_whitespace=True, names=BOLTWOOD_COLUMNS,
                         parse_dates={"timestamp":[2,1,0,3,4,5]}, index_col=0)

if __name__=="__main__":
    print(read_boltwood(argv[1]))
