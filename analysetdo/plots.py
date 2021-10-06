import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools as it
import numpy as np
from dataclasses import dataclass
from typing import Optional
from abc import ABC


def setup_matplotlib():
    mpl.rcdefaults()
    mpl.rcParams["font.size"] = 12  # change the size of the font in every figure
    mpl.rcParams["font.family"] = "Arial"  # font Arial in every figure
    mpl.rcParams["axes.labelsize"] = 12
    mpl.rcParams["xtick.labelsize"] = 12
    mpl.rcParams["ytick.labelsize"] = 12
    mpl.rcParams["xtick.direction"] = "in"
    mpl.rcParams["ytick.direction"] = "in"
    mpl.rcParams["xtick.top"] = True
    mpl.rcParams["ytick.right"] = True
    mpl.rcParams["xtick.major.width"] = 0.6
    mpl.rcParams["ytick.major.width"] = 0.6
    mpl.rcParams["axes.linewidth"] = 0.6  # thickness of the axes lines
    mpl.rcParams[
        "pdf.fonttype"
    ] = 3  # Output Type 3 (Type3) or Type 42 (TrueType), TrueType allows
    # editing the text in illustrator


class Plotter:
    """lalal"""

    def __init__(self):
        self.plots = list()
        self.fig_size = (8.5, 6)

    def add_plot(self, plot):
        self.plots.append(plot)
        return self

    def add_many_plots(self, plots):
        for plot in plots:
            self.plots.append(plot)
        return self

    def with_fig_size(self, height, width):
        self.fig_size = (height, width)
        return self

    def init_plot(self, num_rows, num_cols):
        fig, axes = plt.subplots(num_rows, num_cols, figsize=self.fig_size)
        if num_rows == 1 and num_cols == 1:
            axes = np.array([[axes]])
        elif num_rows == 1 or num_cols == 1:
            axes = np.array([axes])
        fig.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.9)
        return fig, axes

    def plot(self, num_rows, num_cols):
        fig, axes = self.init_plot(num_rows, num_cols)
        for ((row, col), plot) in zip(
            it.product(range(num_rows), range(num_cols)), self.plots
        ):
            plot.draw_into(axes[row, col])
        return fig, axes


class AbstractPlot(ABC):
    def __add__(self, other):
        return combine_plots([self, other])


class PlotSignalVsField(AbstractPlot):
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


@dataclass(frozen=True)
class PlotFitBounds(AbstractPlot):
    low: float
    high: float

    def draw_into(self, axe):
        axe.axvline(self.high, color="gray")
        axe.axvline(self.low, color="gray")


@dataclass(frozen=True)
class PlotInfo(AbstractPlot):
    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    legend: bool = False

    def draw_into(self, axe):
        if self.title is not None:
            axe.set_title(self.title)
        if self.xlabel is not None:
            axe.set_xlabel(self.xlabel)
        if self.ylabel is not None:
            axe.set_ylabel(self.ylabel)
        if self.legend:
            axe.legend()
        return axe


def combine_plots(plots):
    return PlotCombination(plots)


class PlotCombination(AbstractPlot):
    def __init__(self, plots):
        self.plots = plots

    def draw_into(self, axe):
        for plot in self.plots:
            plot.draw_into(axe)
        return axe


def standard_signal_vs_field_plot(data):
    return combine_plots(
        [
            PlotSignalVsField().add_data(data.up, "UP").add_data(data.down, "DOWN"),
            PlotInfo(
                title="Signal vs Field",
                xlabel="Field ( T )",
                ylabel="Signal",
                legend=True,
            ),
        ]
    )


def standard_signal_without_background_vs_field_plot(data):
    return combine_plots(
        [
            PlotSignalVsField().add_data(data.up, "UP").add_data(data.down, "DOWN"),
            PlotInfo(
                title="Signal without background vs Field",
                xlabel="Field ( T )",
                ylabel="Signal without background",
                legend=True,
            ),
        ]
    )


def standard_background_vs_field_curves(data):
    return (
        PlotSignalVsField()
        .add_data(data.up, "UP_fit", color="k")
        .add_data(data.down, "DOWN_fit", color="gray")
    )
