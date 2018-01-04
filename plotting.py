import matplotlib.pyplot as plt
import numpy as np

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
			plt.legend()
		if not self.savefile is None:
			fig.savefig(self.savefile)
		else:
			plt.show()

