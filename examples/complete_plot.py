import analysetdo as tdo
from analysetdo import plots 
import numpy as np
import matplotlib.pyplot as plt

# Parameters
low_bound_fit = 50 
high_bound_fit = 86
degree_fit = 3
num_fit_samples = 1000 #number of points in the fit
fit_domain = np.linspace(low_bound_fit, high_bound_fit, num_fit_samples)

low_bound_fft = 60
high_bound_fft = 80
num_samples_fft = 1000
fft_domain = np.linspace(1/low_bound_fft, 1/high_bound_fft, num_samples_fft)

# Load and clean data
data = tdo.read_from_file("data_test_2.out")  # read the file
data = data.remove_field_less_than(1e-3).split_up_down()  # clean data

# Initialize plot
manager = plots.PlotManager()

# Plot raw data
manager.add_plot(
	plots.PlotSignalVsField()
		.add_data(data.up, "UP")
		.add_data(data.down, "DOWN")
	+ plots.PlotInfo(
		title="Signal vs Field",
		xlabel="Field ( T )",
		ylabel="Signal",
		legend=True,
    ),
)

# Fit background from polynomial
backgrounds = data.map(tdo.poly_background_fit(low_bound_fit, high_bound_fit, degree_fit))
fitted_background = backgrounds.map(tdo.background_fit(fit_domain))

# Plot raw data with background fit
manager.add_plot(
	plots.PlotFitBounds(low_bound_fit, high_bound_fit)
	+ plots.PlotSignalVsField()
		.add_data(fitted_background.up, "Fit UP", color="black")
		.add_data(fitted_background.down, "Fit DOWN", color="gray")
	+ plots.PlotSignalVsField()
		.add_data(data.up, "Signal UP")
		.add_data(data.down, "Signal DOWN")
	+ plots.PlotInfo(
		title="Signal vs Field",
		xlabel="Field ( T )",
		ylabel="Signal",
		legend=True,
    ),
)

# Remove background from raw data
filters = backgrounds.map(tdo.background_filter)
data_without_background = data.map_each(filters)

# Plot data without background
manager.add_plot(
	plots.PlotFitBounds(low_bound_fit, high_bound_fit)
	+ plots.PlotSignalVsField()
		.add_data(data_without_background.up, "UP")
		.add_data(data_without_background.down, "DOWN")
    + plots.PlotInfo(
		title="Signal without background vs Field",
		xlabel="Field ( T )",
		ylabel="Signal without background",
		legend=True,
	),
)

# Compute derivative
derivatives = data.map(tdo.gradient).map(lambda dat: dat.remove_field_less_than(1))

# Plot derivatives
manager.add_plot(
	plots.PlotSignalVsField().add_data(derivatives.up, "UP").add_data(derivatives.down, "DOWN")
    + plots.PlotInfo(
		title="Derivatives vs Field",
		xlabel="Field ( T )",
		ylabel="Derivatives",
		legend=True,
	),
)

# Remove background from derivative
backgrounds_derivative = derivatives.map(
    tdo.poly_background_fit(low_bound_fit, high_bound_fit, degree_fit)
)
fitted_background_derivative = backgrounds_derivative.map(tdo.background_fit(fit_domain))
filters_derivative = backgrounds_derivative.map(tdo.background_filter)
derivative_without_background = derivatives.map_each(filters_derivative)

# Data without background inverted field 
data_without_background_inverse_field = data_without_background.map(
    lambda dat: dat.trim_before_field(low_bound_fit)
    .trim_after_field(high_bound_fit)
    .inverse_field()
)

# Plot data no back inv field
manager.add_plot(
	plots.PlotSignalVsField()
        .add_data(data_without_background_inverse_field.up, "UP")
        .add_data(data_without_background_inverse_field.down, "DOWN")
    + plots.PlotInfo(
		title="Signal without background vs Inverse field",
		xlabel="Inverse field ( 1 / T )",
		ylabel="Signal without background",
		legend=True,
	),
)

# Fourier transform
fft_data = data_without_background_inverse_field.map(
    lambda dat: dat.resample(fft_domain).fourier_transform()
)

manager.add_plot(
	plots.PlotSignalVsField()
        .add_data(fft_data.up, "UP")
        .add_data(fft_data.down, "DOWN")
    + plots.PlotInfo(
		title="Fourier transform from inverse field",
		xlabel="Frequencies ( T )",
		ylabel="Amplitudes",
		legend=True,
	),
)

# Render plot
manager.with_fig_size(12, 8).plot(2, 3)
plt.show()
