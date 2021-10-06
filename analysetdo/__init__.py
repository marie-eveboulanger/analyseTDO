from collections.abc import Callable
from dataclasses import dataclass
import numpy as np
from numpy.polynomial import polynomial as pol


def read_from_file(file_name: str):
    """Load the target file as SweepData.

    Assume that the file contains 2 columns,
    where the first one is the field and the
    second one the TDO signal.

    """
    data = np.loadtxt(file_name)
    field = data[:, 0]
    signal = data[:, 1]
    return SweepData(field, signal)


@dataclass(frozen=True)
class SweepData:
    """Data from TDO experiment.

    Arguments
    ---------
    field:
        magnetic field in Tesla, both up and down sweeps
    signal:
        TDO signal corresponding to the field
    """

    field: np.ndarray
    signal: np.ndarray

    def remove_field_less_than(self, threshold):
        """Remove values, in both signal and field, where field is lower than threshold.

        This returns a new SweepData object. It is mean to be chain with other methods.
        """
        above = np.nonzero(self.field >= threshold)[0]
        field = self.field[above]
        signal = self.signal[above]
        return SweepData(field, signal)

    def split_up_down(self):
        """Split the TDO field and signal for the up sweep and down sweep.

        Assume that the field is sorted in increasing order up to
        its maximum value corresponding to the up sweep. And in
        decreasing order from that point corresponding to the down sweep.

        The field and signal from the down sweep are reversed so that the
        field is in increasing order.
        """
        separator = np.argmax(self.field) + 1
        field_up, field_down = self.field[:separator], self.field[separator:]
        signal_up, signal_down = self.signal[:separator], self.signal[separator:]
        return UpDownData(
            SweepData(field_up, signal_up),
            SweepData(np.flip(field_down), np.flip(signal_down)),
        )

    def trim_before_field(self, target):
        index = self.nearest_field_index(target) + 1
        return SweepData(self.field[index:], self.signal[index:])

    def trim_after_field(self, target):
        index = self.nearest_field_index(target) + 1
        return SweepData(self.field[:index], self.signal[:index])

    def nearest_field_index(self, target):
        """Find the index where the field is the closest to target."""
        above = np.nonzero(self.field >= target)[0][0]
        below = above - 1
        if np.abs(self.field[above] - target) <= np.abs(self.field[below] - target):
            return above
        else:
            return below


@dataclass(frozen=True)
class UpDownData:
    """Field and signal for both up and down sweeps.

    All data is assumed to be sorted from up and down fields.
    """

    up: SweepData
    down: SweepData

    def map(self, function):
        """Apply the function to both up and down values"""
        up = function(self.up)
        down = function(self.down)
        return UpDownData(up, down)

    def map_each(self, functions):
        """Apply the up function to the up value and the down function to the down value"""
        up = functions.up(self.up)
        down = functions.down(self.down)
        return UpDownData(up, down)    


# Filters


def background_filter(background):
    filt = lambda data: SweepData(data.field, data.signal - background(data.field))
    return filt

def background_fit(field):
    return lambda background: SweepData(field, background(field))
    

def poly_background_fit(low_bound, high_bound, degree):
    def fit(data):
        trimmed = data.trim_before_field(low_bound).trim_after_field(high_bound)
        coefficients = pol.polyfit(trimmed.field, trimmed.signal, degree)
        background = pol.Polynomial(coefficients)
        return background
    return fit


def smooth_background_fit(low_bound, high_bound, degree):
    def fit(data):
        trimmed = data.trim_before_field(low_bound).trim_after_field(high_bound)
        coefficients = pol.polyfit(trimmed.field, trimmed.signal, degree)
        background = pol.Polynomial(coefficients)
        return background
    return fit

















