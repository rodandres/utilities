import pandas as pd
from python_utilities.plotting.dataplot import DataPlotter

df = pd.read_csv('files_to_use/RRC3_FLIGHT_DATA_2025_IREC.csv')

data_to_plot = DataPlotter(df)
data_to_plot.show_info()

#y_data = ['Altitude', 'Velocity', 'Temperature']
y_data = ['Altitude', 'Velocity']

data_to_plot.general_plot('Time', y_data,
                          title="Flight Data Overview",
                          xlabel="Time [s]",
                          ylabel="Meters [m]"
                          )