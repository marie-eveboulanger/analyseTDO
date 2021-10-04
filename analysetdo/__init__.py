from dataclasses import dataclass
import numpy as np


def read_from_file(file_name: str):
    """ Load the target file as SweepData.

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
    """ Data from TDO experiment.

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
        """ Remove values, in both signal and field, where field is lower than threshold.
        
        This returns a new SweepData object. It is mean to be chain with other methods.
        """
        above = np.nonzero(self.field >= threshold)[0]
        field = self.field[above]
        signal = self.signal[above]
        return SweepData(field, signal)

    def split_up_down(self):
        """ Split the TDO field and signal for the up sweep and down sweep.

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
            field_up, signal_up, np.flip(field_down), np.flip(signal_down)
        )


@dataclass(frozen=True)
class UpDownData:
    """ Field and signal for both up and down sweeps.

    All data is assumed to be sorted from up and down fields.
    """
    field_up: np.ndarray
    signal_up: np.ndarray
    field_down: np.ndarray
    signal_down: np.ndarray

