import analysetdo as tdo
import analysetdo.plots as tdop
import numpy as np
import matplotlib.pyplot as plt 


# Data processing
data = tdo.read_from_file("data_test.out") # read the file
data = data.remove_field_less_than(1e-3).split_up_down() # clean data

data_without_background = data.map(tdo.poly_background_filter(30,50,4))


# Data plotting

tdop.setup_matplotlib()

plotter = tdop.Plotter().add_many_plots([
    tdop.PlotSignalVsField().add_data(data.up, "UP").add_data(data.down, "DOWN"),
    tdop.PlotSignalVsField().add_data(data_without_background.up, "UP").add_data(data_without_background.down, "DOWN"),
])

plotter.plot(1,2)

plt.show()