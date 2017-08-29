import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas_reader import read_boltwood, read_clouds
from plot_tools import fractional_bar_plot
from sys import argv

def plot_skytemp_clouds(data):
    sns.violinplot(x="clouds", y="skyTemp", data=data)

def plot_month_clouds(data):
    sns.countplot(x="month", hue="clouds", data=data)

def plot_month_rain(data):
    sns.countplot(x="month", hue="rain", data=data)

def plot_hour_dark_clouds(data):
    selection = data.loc[(data["daylight"]=="dark") & (data["clouds"]=="clear")]
    sns.countplot(x="hour", data=selection, color="black")

def plot_month_dark_clouds(data):
    selection = data.loc[(data["daylight"] == "dark")]
    fractional_bar_plot(x="month", hue="clouds", data=selection, palette="Blues_r",
                        labelsH=["clear", "cloudy", "very cloudy", "unknown"])

def plot_month_humidity(data):
    selection = data.loc[(data["clouds"]!="unknown")]
    sns.boxplot(x="month", y="humidity", hue="clouds", data=selection)

def plot_month_clouds_grid(data):
    selection = data#.loc[(data["clouds"]!="unknown")]
    sns.countplot(x="month", hue="clouds", data=selection)


def compare_Nuuksio_clouds(data, cloud_file):
    FMI_data = read_clouds(cloud_file).sort_index()
    start,end = FMI_data.index[0], FMI_data.index[-1]
    selection = data.loc[data["skyTemp"]>-200].reindex(FMI_data.index, method="pad")
    X = selection["skyTemp"]
    Y = FMI_data["cloudCover"]
    data = pd.concat([X, Y], axis=1)
    sns.boxplot(x="cloudCover", y="skyTemp", data=data)

    


if __name__=="__main__":
    print("Reading data...")
    data = read_boltwood(argv[1]).sort_index()
    print(data.index[0], data.index[-1])
    
    print("Making plot...")
    plot_month_dark_clouds(data)
    
    print("Showing plot...")
    plt.show()
