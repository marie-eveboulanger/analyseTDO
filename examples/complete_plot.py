import analysetdo as tdo
from analysetdo import plots 
import numpy as np
import matplotlib.pyplot as plt

# Parameters
low_bound_fit = 50
high_bound_fit = 86
degree_fit = 3
num_fit_samples = 1000

# Load and clean data
data = tdo.read_from_file("data_test_2.out")  # read the file
data = data.remove_field_less_than(1e-3).split_up_down()  # clean data

# Initialize plot
plotter = plots.Plotter()

# Plot raw data
plotter.add_plot(plots.standard_signal_vs_field_plot(data))

# Fit background from polynomial
fit_domain = np.linspace(low_bound_fit, high_bound_fit, num_fit_samples)
backgrounds = data.map(tdo.poly_background_fit(low_bound_fit, high_bound_fit, degree_fit))
fitted_background = backgrounds.map(tdo.background_fit(fit_domain))

# Plot raw data with background fit
plotter.add_plot(
	plots.PlotFitBounds(low_bound_fit, high_bound_fit)
    + plots.standard_background_vs_field_curves(fitted_background)
    + plots.standard_signal_vs_field_plot(data)
)

# Remove background from raw data
filters = backgrounds.map(tdo.background_filter)
data_without_background = data.map_each(filters)

# Plot data without background
plotter.add_plot(
	plots.PlotFitBounds(low_bound_fit, high_bound_fit)
	+ plots.standard_signal_without_background_vs_field_plot(data_without_background)
)

# Compute gradient
gradient = data.map(tdo.gradient)

# Render plot

plotter.with_fig_size(12, 8).plot(2, 3)
plt.show()