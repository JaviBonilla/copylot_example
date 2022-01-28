import json
import utils_copylot as uc
import utils_plotly as up
from copylot import CoPylot

spt_filename = './assets/default.spt'
weather_filename = './assets/TMY_37.095_-2.358549.epw'

# Initialization
cp = CoPylot()
r = cp.data_create()

# Creates a callback function for message transfer
cp.api_callback_create(r)

# Load spt file
uc.load_spt_file(spt_filename, cp, r)

# Set weather file
cp.data_set_string(r, 'ambient.0.weather_file', weather_filename)

# Generate layout
cp.generate_layout(r)
field = cp.get_layout_info(r)

# Simulate
cp.simulate(r)

# Get summary
summary = cp.summary_results(r)
print(json.dumps(summary, indent=2))

# Get flux map
flux = cp.get_fluxmap(r)

# Receiver width and height
rec_width = cp.data_get_number(r, 'receiver.0.rec_width')
rec_height = cp.data_get_number(r, 'receiver.0.rec_height')

# Flux map figure
fig = up.fig_receiver_flux(flux, rec_width, rec_height)

# Show figure
fig.show()

# Free data
cp.data_free(r)
