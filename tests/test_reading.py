import analysetdo as tdo
import numpy as np


def test_read_from_file():
    data = tdo.read_from_file("tests/data_test.out")
    up_down = data.remove_field_less_than(1e-3).split_up_down()
    np.testing.assert_array_equal(up_down.up.field, np.sort(up_down.up.field))
    np.testing.assert_array_equal(up_down.down.field, np.sort(up_down.down.field))


def dummy_sweep_data():
    field = np.array([-2, 0.1, -1, 1, 2, 3, 4, 3, 2, 1, -0.1, 0.2])
    signal = np.array([2, 4, 3, 5, 6, 7, 2, 3, 4, 9, 8, 4])
    return tdo.SweepData(field, signal)


def test_convert_dummy_to_up_down():
    up_down = dummy_sweep_data().split_up_down()
    np.testing.assert_array_equal(up_down.up.field, np.array([-2, 0.1, -1, 1, 2, 3, 4]))
    np.testing.assert_array_equal(up_down.up.signal, np.array([2, 4, 3, 5, 6, 7, 2]))
    np.testing.assert_array_equal(up_down.down.field, np.array([0.2, -0.1, 1, 2, 3]))
    np.testing.assert_array_equal(up_down.down.signal, np.array([4, 8, 9, 4, 3]))


def test_remove_negative_from_dummy_data():
    data = dummy_sweep_data().remove_field_less_than(0.5)
    np.testing.assert_array_equal(data.field, np.array([1, 2, 3, 4, 3, 2, 1]))
    np.testing.assert_array_equal(data.signal, np.array([5, 6, 7, 2, 3, 4, 9]))


def test_remove_neg_and_convert_to_up_down():
    up_down = dummy_sweep_data().remove_field_less_than(0.5).split_up_down()
    np.testing.assert_array_equal(up_down.up.field, np.array([1, 2, 3, 4]))
    np.testing.assert_array_equal(up_down.up.signal, np.array([5, 6, 7, 2]))
    np.testing.assert_array_equal(up_down.down.field, np.array([1, 2, 3]))
    np.testing.assert_array_equal(up_down.down.signal, np.array([9, 4, 3]))
