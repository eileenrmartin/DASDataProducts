import sys
import h5py
import numpy as np
#with h5py.File("/opt/trebleserver/data/UTC-YMD20200528/combined_data.vhdf5", "r") as→f:
filename = sys.argv[1]
f = h5py.File(filename, 'r')
time = f["time"][:] # Load time into memory
strain_rate = f["strain_rate"] # Prepare strain rate data but don't˓→load
index_min = np.argmax(time>=1590649049) # Find the index within a time range→(1s)
index_max = np.argmax(time>=159064049)
data = strain_rate[index_min:index_max, :] # Only extract the desired data from→the associated source files
print(data.shape)