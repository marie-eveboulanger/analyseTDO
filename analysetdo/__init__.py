from collections.abc import Callable
from dataclasses import dataclass
import numpy as np
from numpy.polynomial import polynomial as pol


def read_from_file(file_name: str):
    """Load the target file as SweepData.

    Assume that the file contains 2 columns,
    where the first one is the field and the
    second one the TDO signal.

    Args:
        file_name: path to where the file is.

    Returns:
        Raw Sweep Data

    """
    data = np.loadtxt(file_name)
    field = data[:, 0]
    signal = data[:, 1]
    return SweepData(field, signal)


@dataclass(frozen=True)
class SweepData:
    """Data from TDO experiment.

    Args:
        field: magnetic field in Tesla
        signal: TDO signal corresponding to the field
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
        """Cut the data before a targeted value

        Args:
            target: all field above will be kept

        """
        index = self.floor_field_index(target)
        return SweepData(self.field[index:], self.signal[index:])

    def trim_after_field(self, target):
        """Cut the data after a targeted value"""
        index = self.ceil_field_index(target)
        return SweepData(self.field[:index], self.signal[:index])

    def nearest_field_index(self, target):
        """Find the index where the field is the closest to target."""
        above = np.nonzero(self.field >= target)[0][0]
        below = above - 1
        if np.abs(self.field[above] - target) <= np.abs(self.field[below] - target):
            return above
        else:
            return below

    def floor_field_index(self, target):
        """Find the index where the field is the closest to target. Rounding below."""
        above = np.nonzero(self.field > target)[0][0]
        below = above - 1
        return below

    def ceil_field_index(self, target):
        """Find the index where the field is the closest to target. Rounding above."""
        above = np.nonzero(self.field >= target)[0][0]
        return above

    def inverse_field(self):
        inverse_field = 1/self.field
        return SweepData(inverse_field[::-1], self.signal[::-1])

    def resample(self, domain):
        signal = np.interp(domain, self.field, self.signal)
        return SweepData(domain, signal)

    def fourier_transform(self):
        """We assume that the field is sampled uniformly"""    
        delta = np.mean(np.diff(self.field))
        frequences = np.fft.fftfreq(len(self), d=delta)
        amplitudes = np.fft.fft(self.signal)
        cutoff = np.int(np.ceil(len(self) / 2) - 1)
        pos_indices = frequences >0
        return SweepData(frequences[pos_indices], np.abs(amplitudes)[pos_indices])

    def __len__(self):
        return len(self.field)


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


# Transformations


def background_filter(background):
    """Creates the filtered data"""
    filt = lambda data: SweepData(data.field, data.signal - background(data.field))
    return filt


def background_fit(field):
    """Creates a fit function"""
    return lambda background: SweepData(field, background(field))


def poly_background_fit(low_bound, high_bound, degree):
    """Creates a background function from a polynomial fit"""

    def fit(data):
        trimmed = data.trim_before_field(low_bound).trim_after_field(high_bound)
        coefficients = pol.polyfit(trimmed.field, trimmed.signal, degree)
        background = pol.Polynomial(coefficients)
        return background

    return fit


def gradient(data):
    """Give back the derivative of the signal"""
    signal_derivative = np.gradient(data.signal, data.field)
    return SweepData(data.field, signal_derivative)


def fourier_transform(low_bound, high_bound, delta):
    def transform(data):
        domain = np.arange(low_bound, high_bound, delta)
        resampled = data.resample(domain)
        frequences = np.fft.fftfreq(len(domain), d=delta)
        amplitudes = np.fft.fft(resampled.signal)
        cutoff = np.ceil(len(domain / 2)) - 1
        return SweepData(frequences[0:cutoff], amplitudes[0:cutoff])

    return transform


























    
