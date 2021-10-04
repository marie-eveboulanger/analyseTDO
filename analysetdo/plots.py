import matplotlib as mpl
import matplotlib.pyplot as plt 
import itertools as it
import numpy as np 

def setup_matplotlib():
	mpl.rcdefaults()
	mpl.rcParams['font.size'] = 12 # change the size of the font in every figure
	mpl.rcParams['font.family'] = 'Arial' # font Arial in every figure
	mpl.rcParams['axes.labelsize'] = 12
	mpl.rcParams['xtick.labelsize'] = 12
	mpl.rcParams['ytick.labelsize'] = 12
	mpl.rcParams['xtick.direction'] = "in"
	mpl.rcParams['ytick.direction'] = "in"
	mpl.rcParams['xtick.top'] = True
	mpl.rcParams['ytick.right'] = True
	mpl.rcParams['xtick.major.width'] = 0.6
	mpl.rcParams['ytick.major.width'] = 0.6
	mpl.rcParams['axes.linewidth'] = 0.6 # thickness of the axes lines
	mpl.rcParams['pdf.fonttype'] = 3  # Output Type 3 (Type3) or Type 42 (TrueType), TrueType allows
										# editing the text in illustrator


class Plotter:
	""" lalal"""
	def __init__(self):
		self.plots = list()

	def add_plot(self, plot):
		self.plots.append(plot)
		return self

	def add_many_plots(self, plots):
		for plot in plots:
			self.plots.append(plot)
		return self

	def init_plot(self, num_rows, num_cols):
		fig, axes = plt.subplots(num_rows, num_cols,figsize=(8.5,6)) 
		if num_rows == 1 and num_cols == 1:
			axes = np.array([[axes]])
		elif num_rows == 1 or num_cols == 1:
			axes = np.array([axes])
		fig.subplots_adjust(left=0.15, right=.9, bottom=0.15, top=0.9);
		return fig, axes
		
	def plot(self, num_rows, num_cols):
		fig, axes = self.init_plot(num_rows, num_cols)
		for ((row, col), plot) in zip(it.product(range(num_rows), range(num_cols)), self.plots):
			plot.draw_into(axes[row,col])
		return fig, axes


class PlotSignalVsField:
	def __init__(self):
		self.data = dict()

	def add_data(self, data, label, **kwargs):
		self.data[label] = (data, kwargs)
		return self

	def draw_into(self, axe):
		for label, data_and_kwargs in self.data.items():
			data = data_and_kwargs[0]
			kwargs = data_and_kwargs[1]
			axe.plot(data.field, data.signal, label=label, **kwargs)
		return axe
































