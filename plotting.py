import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class PlotElement:
    def __init__(self, title, values):
        self.title = title
        self.values = values

class Plot:
    def __init__(self, title, xlabel, ylabel, savefile = None):
        self.value_list = []
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.savefile = savefile
        
    def append_values(self, title, values, pre_proccess = False):
        if pre_proccess:
            newvals = list(map(lambda x: round(x, 5), values))
        else:
            newvals = values
        self.value_list.append(PlotElement(title, newvals))
    
    def plot(self):
        raise NotImplementedError('you must implement this method')

class LinePlot(Plot):
    def __init__(self, title, xlabel, ylabel, savefile = None, legend = False):
        super(LinePlot, self).__init__(title, xlabel, ylabel, savefile)
        self.legend = legend
    def plot(self):
        fig = plt.figure()
        ran = max([len(v.values) for v in self.value_list])
        xran = np.arange(ran)
        
        for v in self.value_list:
            plt.plot(xran, v.values, label = v.title)
        
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        
        if self.legend:
            plt.legend(loc=9, bbox_to_anchor=(0.5,-0.1), ncol=2)
        if not self.savefile is None:
            fig.savefig(self.savefile)
        else:
            plt.show()

class PercentHistogram(Plot):
    def __init__(self, title, xlabel, ylabel, savefile = None, legend = False):
        super(PercentHistogram, self).__init__(title, xlabel, ylabel, savefile)
        self.legend = legend
    def plot(self):
        fig = plt.figure
        sumval = sum(x.values for x in self.value_list)
        frequencies = [x.values/sumval for x in self.value_list]
        labels = [x.title for x in self.value_list]
        
        # For our own labels
        fig = plt.figure()
        
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        
        pd.Series(frequencies, index=labels).plot(kind='bar', color='rgb')
        
        if self.legend:
            plt.legend(loc=9, bbox_to_anchor=(0.5,-0.1), ncol=2)
        if not self.savefile is None:
            fig.savefig(self.savefile)
        else:
            plt.show()
