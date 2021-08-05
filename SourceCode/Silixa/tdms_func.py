""" TDMS Combine Files Functions

This module uses the condenser.py and tdms_func.py functions to create data products for individual tdms files and 
combine them to be saved in files. Indices arrays with information about time, channels, and frequency are created
to give the reader of the files useful info. When creating the individual spectral tensors similar frequency bins 
can also be further condensed. A tdms_params.py file is needed to define the condenser function parameters. 
A TDMSReader script (from Silixa) is used to read in original DAS data.

Functions
---------
create_file_names - Creates list of file names
ch_ind_array - Create the channel info array
tw_ind_array - Create the time info array
freq_ind_array - Create the frequency info array
combine_data_products - Create big tensor and stat arrays
"""

import sys
sys.path.insert(1, '..')
from Silixa.tdms_reader import TdmsReader
import condenser
import numpy as np
import matplotlib.pyplot as plt
from Silixa import tdms_params as tp
from datetime import datetime, timedelta
import pytz


def create_file_names():
    """
    Create the array of filenames to use for the big tensor, based on the date and time values from the 
    params file. 
    
    Returns
    -------
    array
        File names
    """
    
    #file path names
    file_paths = []
    
    #find time difference in file range
    hour_diff = tp.file_hour_end - tp.file_hour_start
    min_diff = 0
    if tp.file_min_end > tp.file_min_start:
        min_diff = tp.file_min_end - tp.file_min_start
    else:
        hour_diff = hour_diff - 1
        min_diff = (tp.file_min_end + 60) - tp.file_min_start

    #calc number of files
    n_files = (hour_diff * 60) + min_diff + 1 

    hour_count = tp.file_hour_start
    min_count = tp.file_min_start

    for i in range(n_files):
        #add filename to list of files
        name = 'PSUDAS_UTC_' + str(tp.file_year) + '{:02}'.format(tp.file_month) + '{:02}'.format(tp.file_day) + '_' + '{:02}'.format(hour_count) + '{:02}'.format(min_count) + tp.file_end
        file_paths.append(name)
        #increment minutes and hour if applicable
        if min_count < 59:
            min_count = min_count + 1 
        else:
            min_count = 0
            hour_count = hour_count + 1
    
    return file_paths


def ch_ind_array(num_sensor_groups):
    """
    Create the array to hold information about channels, including the number of channel groups
    and the indexes in the original data array of the start and ending channels in each channel group 
    
    Parameters
    ----------
    num_sensor_groups : int
        Number of channel groups
    
    Returns
    -------
    array
        Channel information
    """

    #create 1d array to hold channel information
    channel_inds = np.zeros((num_sensor_groups * 2) + 1)
    
    #add ch info to channel indices array
    channel_inds[0] = num_sensor_groups       #number of channel groups   
    #store start and end channel in each group 
    for k in range(num_sensor_groups):
        #calculate start and end channel numbers
        start_channel = k * tp.ch_group_size
        end_channel = start_channel + tp.ch_group_size - 1
        #check for if channel groups not divisible
        if k == (num_sensor_groups - 1):
            end_channel = tp.last_channel
        channel_inds[2*k + 1] = start_channel   
        channel_inds[2*k + 2] = end_channel
    
    return channel_inds


def tw_ind_array(fs, num_files, num_time_windows):
    """
    Create the array to hold information about time, including the length of each time window in 
    seconds and datetime objects holding the starting time in UTC for the start of each time window
    
    Parameters
    ----------
    fs : int
        Sampling frequency of original data
    num_files : int
        Number of files to combine
    num_time_windows : int
        Number of time windows 
    
    Returns
    -------
    array
        Time information
    """
    
    #create 1d array to hold time information
    time_inds = []
    
    #add time info to time window indices array
    wind_length = int(tp.time_window / fs)    #length of window in secs
    time_inds.append(wind_length)
    time_inds.append(num_time_windows)        #number of time windows
    
    #add datetime objs of UTC start time of windows
    start_hour = tp.file_hour_start
    start_min = tp.file_min_start
    #start datetime obj of first file
    start_dttime = datetime(tp.file_year, tp.file_month, tp.file_day, start_hour, start_min, 0, 0, tzinfo=pytz.UTC)   
    total_microseconds = num_files * 60 * 1000000       #total number of microseconds in all files
    
    #add datetime start time for each time window
    for j in range(0, total_microseconds, (wind_length * 1000000)):
        time_inds.append(start_dttime + timedelta(microseconds=j))
    
    return time_inds


def freq_ind_array(nyq_freq, num_cond_freqs):
    """
    Create the array to hold information about frequency, including the number of frequency bins,
    the width of each frequency bin in Hz, and the nyquist frequency in Hz. 
    
    Parameters
    ----------
    nyq_freq : int
        Nyquist frequency of original data
    num_cond_freqs : int
        Number of frequency bins after condensing 
    
    Returns
    -------
    array
        Frequency information
    """
    
    #create 1d array to hold frequency information
    freq_inds = np.zeros(3)

    #add freq info to freq indices array
    width_freq_bins = nyq_freq / num_cond_freqs 
    freq_inds[0] = num_cond_freqs           #number of freq bins
    freq_inds[1] = width_freq_bins          #width of freq bins
    freq_inds[2] = nyq_freq                 #nyquist frequency
    
    return freq_inds


def combine_data_products(num_files, num_time_windows, num_sensor_groups, num_cond_freqs, file_paths, nyq_freq):
    """
    Create the big tensor holding the individual spectra and store the calculated statistics 
    
    Parameters
    ----------
    num_files : int
        Number of files to iterate through
    num_time_windows : int
        Number of time windows
    num_sensor_groups : int
        Number of channel groups
    num_cond_freqs : int
        Number of frequencies to condense to 
    file_paths : array
        List of file names to look at
    nyq_freq : float
        Nyquist frequency
    Returns
    -------
    tuple
        Arrays for big tensor, and statistics in the frequency domain (standard deviations, means, maximum values, and peak frequency)
    """
    
    #create big tensor to hold all spectra
    #params same for each file, so tensor bigger lengthwise
    big_tens = np.zeros((num_files * num_time_windows, num_sensor_groups, num_cond_freqs))
    
    #data products
    
    #standard deviations for channels per each file
    n_channels = tp.last_channel - tp.first_channel + 1
    ch_stds = np.zeros((num_files, num_time_windows, num_sensor_groups))
    
    ch_means = np.zeros((num_files, n_channels))
    
    #max value for each channel per file
    ch_maxs = np.zeros((num_files, n_channels))
    
    #peak frequency per file
    peak_freqs = np.zeros(num_files)
    
    #times
    stds_t = np.zeros((num_files, n_channels))
    means_t = np.zeros((num_files, n_channels))
    maxs_t = np.zeros((num_files, n_channels))
    
    #write each of files to cond file
    for i in range(len(file_paths)):
        #pull file from list
        fp = file_paths[i]
        
        #get tdms reader
        tdms = TdmsReader(fp)
        #read in tdms data - array of time samples x channels
        some_data = tdms.get_data(tp.first_channel, tp.last_channel, tp.first_time_sample, tp.last_time_sample)
        
        #calculate number of frequencies to store
        num_freq = condenser.calc_num_freq(len(some_data), num_time_windows)
        
        #get condensed matrix
        spect, std_devs, means, max_vals, peak_freq = condenser.condmatrix(some_data, num_time_windows, tp.time_window, num_sensor_groups, tp.ch_group_size, tp.last_channel, num_freq, nyq_freq)
        
        #avg similar frequencies to get smaller number of freq bins and frequencies to store
        spect = spect.reshape(num_time_windows, num_sensor_groups, num_freq // tp.bin_size, tp.bin_size)
        spect = np.mean(spect, axis=-1)
        
        #store spect in tensor
        t_indx = i * num_time_windows
        c_indx = num_sensor_groups
        big_tens[t_indx:t_indx+spect.shape[0], 0:c_indx, :] = spect
        
        #store stats in respective arrays
        ch_stds[i, :, :] = std_devs
        ch_means[i, :] = means
        ch_maxs[i, :] = max_vals
        peak_freqs[i] = peak_freq
        
        means_t[i, :] = condenser.mean_time(some_data)
        stds_t[i, :] = condenser.std_dev_time(some_data)
        maxs_t[i, :] = condenser.max_time(some_data)
    
    return big_tens, ch_stds, ch_means, ch_maxs, peak_freqs, means_t, stds_t, maxs_t