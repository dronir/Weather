#import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pandas_reader import read_boltwood, read_clouds
from plot_tools import fractional_bar_plot
from sys import argv
from datetime import datetime

value_by_cloud = {
    "clear" : 0,
    "cloudy" : 1,
    "very cloudy" : 2,
    "unknown" : 3
}

cloud_by_value =  {0:"clear", 1:"cloudy", 2:"very cloudy", 3:"unknown"}

def get_daily(Data, Y, M, D):
    """Get the data for a particular day from a Pandas dataframe.
    The data are mapped to numbers for min/max operation."""
    start = datetime(year=Y, month=M, day=D, hour=0, minute=0)
    end = datetime(year=Y, month=M, day=D, hour=23, minute=59, second=59)
    return Data[start:end]["clouds"].map(value_by_cloud)
    
def hourly_best(Data, Y, M, D):
    "Get the cloud data for a particular day and resample to hourly min."
    daily = get_daily(Data, Y, M, D)["clouds"]
    return daily.resample("H").min().map(cloud_by_value)

def hourly_worst(Data, Y, M, D):
    "Get the cloud data for a particular day and resample to hourly max."
    daily = get_daily(Data, Y, M, D)
    return daily.resample("H").max().map(cloud_by_value)


def get_month(Data, Y, M):
    # Count the number of days by getting the interval between the first of this month to 
    # the first of next month. Need to carry over to next year if M=12.
    Y2 = Y if M < 12 else Y+1
    M2 = M+1 if M < 12 else 1
    Ndays = (datetime(year=Y2, month=M2, day=1) - datetime(year=Y, month=M, day=1)).days
    
    # Get daily data for each day of the month.
    return [hourly_worst(Data, Y, M, m+1) for m in range(Ndays)]


color_by_cloud = {
    "clear" : "#2E78FF",
    "cloudy" : "#6E99E9",
    "very cloudy" : "#99B3E3",
    "unknown" : "#C9CED7",
    np.nan : "black"
}

months = ["", "January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]

def plot_month(Data, Y, M):
    fig = plt.figure(figsize=(10,5))
    dailies = get_month(Data, Y, M)
    N = len(dailies)
    for i, daily_data in enumerate(dailies):
        for j, row in enumerate(daily_data):
            plt.bar(i+1, 1, bottom=j, color=color_by_cloud[row])
    plt.ylim(0,24)
    plt.xlim(0,N+1)
    plt.xlabel("Day of month", fontsize="x-large")
    plt.ylabel("Hour of day", fontsize="x-large")
    plt.title("Metsähovi Boltwood clouds {} {}".format(months[M], Y))
    plt.legend(handles=[mpl.patches.Patch(color=color_by_cloud[key], label=key)
                        for key in color_by_cloud.keys()],
                        loc=2, bbox_to_anchor=(1.0, 1))
    plt.subplots_adjust(left=0.06, bottom=0.1, right=0.85, top=0.9)
    return fig
    


if __name__=="__main__":
    fname = argv[1]
    year = int(argv[2])
    print("Reading data...")
    data = read_boltwood(fname).sort_index()
    print("Start: {}\n  End: {}".format(data.index[0], data.index[-1]))
    
    for i in range(12):
        fig = plot_month(data, year, i+1)
        plt.savefig("clouds_{}_{}.png".format(year, i+1))
    plt.show()
 
    
#    print("Showing plot...")
#    plt.show()
