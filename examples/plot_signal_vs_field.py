import analysetdo as tdo
import analysetdo.plots as tdop
import numpy as np
import matplotlib.pyplot as plt


# Data processing
data = tdo.read_from_file("data_test.out")  # read the file
data = data.remove_field_less_than(1e-3).split_up_down()  # clean data

# Bounds of background fit
low_bound = 30
high_bound = 50
degree_fit = 3

x = np.linspace(low_bound,high_bound, 100)

# Compute the backgrounds from a polynomial fit for up and down
backgrounds = data.map(tdo.poly_background_fit(low_bound, high_bound, degree_fit))
fitted_background = backgrounds.map(tdo.background_fit(x))
filters = backgrounds.map(tdo.background_filter)
data_without_background = data.map_each(filters)

# Data plotting

tdop.setup_matplotlib()

plotter = tdop.Plotter().add_many_plots(
    [
        tdop.PlotFitBounds(low_bound, high_bound) + tdop.standard_background_vs_field_curves(fitted_background) +  tdop.standard_signal_vs_field_plot(data) ,
        tdop.standard_signal_without_background_vs_field_plot(data_without_background),
    ]
)

plotter.with_fig_size(12,6).plot(1, 2)

plt.show()
