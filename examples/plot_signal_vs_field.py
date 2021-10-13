import analysetdo as tdo
import analysetdo.plots as tdop
import numpy as np
import matplotlib.pyplot as plt


# Data processing
data = tdo.read_from_file("data_test_2.out")  # read the file
data = data.remove_field_less_than(1e-3).split_up_down()  # clean data

# Bounds of background fit
low_bound = 50
high_bound = 86
degree_fit = 3

# Bounds for the FFT
low_fft_bound = 60
high_fft_bound = 80
fft_domain = np.linspace(1/low_fft_bound, 1/high_fft_bound, 10000)

x = np.linspace(low_bound, high_bound, 1000)

# Compute the backgrounds from a polynomial fit for up and down
backgrounds = data.map(tdo.poly_background_fit(low_bound, high_bound, degree_fit))
fitted_background = backgrounds.map(tdo.background_fit(x))
filters = backgrounds.map(tdo.background_filter)
data_without_background = data.map_each(filters)

# Derivative
derivatives = data.map(tdo.gradient)

# Remove background from derivative

backgrounds_derivative = derivatives.map(
    tdo.poly_background_fit(low_bound, high_bound, degree_fit)
)
fitted_background_derivative = backgrounds_derivative.map(tdo.background_fit(x))
filters_derivative = backgrounds_derivative.map(tdo.background_filter)
derivative_without_background = derivatives.map_each(filters_derivative)

# Data without background inverted field 

data_without_background_inverse_field = data_without_background.map(
                lambda dat: dat.trim_before_field(low_bound)
                .trim_after_field(high_bound)
                .inverse_field()
            )

# Data plotting

tdop.setup_matplotlib()

plotter = (
    tdop.Plotter()
    # plot raw data
    .add_plot(
        tdop.PlotFitBounds(low_bound, high_bound)
        + tdop.standard_background_vs_field_curves(fitted_background)
        + tdop.standard_signal_vs_field_plot(data)
    )
    # plot raw data minus background
    .add_plot(
        tdop.standard_signal_without_background_vs_field_plot(data_without_background)
    )
    # # plot derivative raw data
    # .add_plot(tdop.standard_derivative_signal_vs_field_plot(derivatives))
    # # plot derivative minus background
    # .add_plot(
    #     tdop.standard_signal_without_background_vs_field_plot(
    #         derivative_without_background
    #     )
    # )
    # plot signal minus background as 1/field
    .add_plot(
        tdop.PlotSignalVsField().add_data(
            data_without_background_inverse_field.up,
            "inverse field",
        )
    )
    # Plot FFT
    .add_plot(
        tdop.standard_FFT_signal_vs_one_over_field_plot(
            data_without_background_inverse_field.map(
                lambda dat: dat.resample(fft_domain).fourier_transform()
            )
        )
    )
)

# Choose how many subplot in the main figure
plotter.with_fig_size(12, 8).plot(2, 3)

plt.show()
