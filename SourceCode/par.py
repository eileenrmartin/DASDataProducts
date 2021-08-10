# parameter file setup for save_data_prod.py: 
# line 4 is the number of channels in each channel group (int),
# line 5 is number of minutes of data to fetch (int), should be same interval as in the crontab file,  
# line 6 is path to directory to save hdf data product files (string)

ch_group_size = 100
min_data = 1
file_path = "."