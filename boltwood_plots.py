import seaborn as sns
import matplotlib.pyplot as plt
from pandas_reader import read_boltwood
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
    selection = data.loc[(data["daylight"]=="dark") & (data["clouds"]=="clear")]
    sns.countplot(x="month", data=selection, color="black")

if __name__=="__main__":
    print("Reading data...")
    data = read_boltwood(argv[1])
    
    print("Making plot...")
    plot_month_dark_clouds(data)
    
    print("Showing plot...")
    plt.show()
