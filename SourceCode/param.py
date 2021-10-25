# parameter file setup for save_data_prod.py: (any parameter files used should have .py extension and have the same parameter names)
# line 6 is ch_group_size, the number of channels in each channel group (int),
# line 7 is min_data, the number of minutes of data to fetch (int), should be same interval as in the crontab file,  
# line 8 is file_path, the path to directory to save hdf data product files (string)
# line 9 is the downsampling factor to use in downsampling data to decimate original signal
# line 10 is the filter order used for the lowpass filter of data

ch_group_size = 10
min_data = 1
file_path = "./files"
downsamp_factor = 2
filterOrder = 4