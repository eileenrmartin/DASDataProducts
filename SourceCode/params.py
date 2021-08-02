#parameter file setup for combine_files.py    

#size of channels and time windows to group together
ch_group_size = 100
#few secs at a time, must be divisible by 500 (sampling rate) - and still must be div by 2
#num time samples must be divisible by time_window - should be a number of frames?
time_window = 1000 

#define bin size to group similar freqs together, should be even divide (no remainder) of num freq aka time_window/2 + 1 - holds for ntimesamples != 30000?
bin_size = 3


