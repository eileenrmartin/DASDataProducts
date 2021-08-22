# parameter file setup for save_data_prod.py: (any parameter files used should have .py extension and have the same parameter names)
# line 6 is ch_group_size, the number of channels in each channel group (int),
# line 7 is min_data, the number of minutes of data to fetch (int), should be same interval as in the crontab file,  
# line 8 is file_path, the path to directory to save hdf data product files (string)

ch_group_size = 100
min_data = 1
file_path = "."