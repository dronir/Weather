import pandas as pd
import seaborn as sns
from numpy import zeros
import matplotlib.pyplot as plt

def fractional_bar_plot(x, hue, data, palette="Blues_d", labelsH=None):
    if labelsH is None:
        labelsH = data[hue].unique()
    nh = len(labelsH)
    
    Groups = data.groupby(x, sort=False)
    Counts = pd.DataFrame()
    for label, group in Groups:
        Counts[label] = group[hue].value_counts(normalize=True)
    data = Counts.transpose()
    nx = len(data.index)
    
    bottom = None
    colors = sns.color_palette(palette, n_colors=nh)
    for i, label in enumerate(labelsH):
        if label in data:
            row = data[label]
        else:
            row = zeros(nx)
        col = "gray" if label=="unknown" else colors[i]
        plt.bar(left=range(nx), height=row, bottom=bottom, color=col, label=label)
        if bottom is None:
            bottom = row
        else:
            bottom = bottom + row
    plt.xticks([x+0.4 for x in range(nx)], data.index)
    plt.ylim(0,1)
    leg = plt.legend(loc="upper center", ncol=len(labelsH), bbox_to_anchor=(0.5, 1.1))
