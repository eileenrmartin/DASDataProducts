#parameter file setup for combine_tdms_files.py

#times range for files in string format, filenames time in format yyyymmdd_hhmm
#year of files
file_year = 2019
#month of files
file_month = 4
file_day = 26
#time range of files, hours of file in 24 hr format
file_hour_start = 20
file_min_start = 54
file_hour_end = 20
file_min_end = 58
#end format of file
file_end = '43.415.tdms'

#range of channels and time samples to pull from data in tdms file
#num of channels: 2432, indexes 0 - 2431
first_channel = 0
last_channel = 2431 
#num of time samples: 30000, indexes 0 - 29999
first_time_sample = 0
last_time_sample = 29999
#sampling frequency
fs = 500    

#size of channels and time windows to group together
ch_group_size = 100
#few secs at a time, must be divisible by 500 (sampling rate) - and still must be div by 2
#num time samples must be divisible by time_window
time_window = 1000 

#define bin size to group similar freqs together, should be even divide (no remainder) of num freq aka time_window/2 + 1 - holds for ntimesamples != 30000?
bin_size = 3