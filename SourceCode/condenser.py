""" Data Product Condenser

This module takes 2D original DAS data of time samples by channels and creates a 3D spectral tensor 
containing the discrete Fourier transform of the data and condensing it into smaller time windows and
channel groups. Descriptive statistics for the transformed data are also calculated including standard deviations
for each time window and channel group combination, means for each time window and channel group, maximum values
for each channel, and peak frequency in Hz. 

Functions
---------

rfft - Real discrete Fourier transform of 2D array
fftfreq - Frequency values of Fourier transformed array
calc_num_ch_groups - Calculate number of channel groups
calc_num_time_win - Calculate number of time windows
calc_num_freq - Calculate number of frequency bins
condmatrix - Create spectral tensor and calculate descriptive statistics

"""

import numpy as np
from scipy import fft
#from scipy import stats
import math



def rfft(some_data):
    """
    Perform a real discrete Fourier transform on a 2D array over the time axis (-2) using scipy Fourier package
    
    Parameters
    ----------
    some_data : array
        2D array of original data read from file/data stream, with rows as time samples and columns as channels
    
    Returns
    -------
    array
        2D array of Fourier transformed data, with rows as frequency bins and columns as channels, same size as some_data
    """

    # fourier transform of array some_data
    data_fft = fft.rfft2(some_data, axes=-2)
    return data_fft


def fftfreq(fs, n_time):
    """
    Calculate the frequency values for corresponding bins of a Fourier transformed array using scipy Fourier package
    
    Parameters
    ----------
    fs : int 
        Sampling frequency of original data in Hz
    n_time : int
        Number of time samples in data 
    
    Returns
    -------
    array
        Array of frequency values of length n_time   
    """

    #sampling freq is used to calculate sample spacing (1 / sampling rate)
    #fftfreq(num samples, sample spacing) -> num samples is len(some_data)
    data_freq = fft.rfftfreq(n_time, d=(1./fs))
    return data_freq


def calc_num_ch_groups(first_channel, last_channel, ch_group_size):
    """
    Calculate the number of condensed channel groups given a group size and number of channels
    
    Parameters
    ----------
    first_channel : int
        Index of the first channel in the data
    last_channel : int
        Index of the last channel in the data
    ch_group_size : int
        Number of channels per group
    
    Returns
    -------
    int
        Number of channel groups
    """
    
    #calculate the total number of channels, add 1 since indexing starts 0 (last_channel - first_channel + 1)
    #divide by group size to get number of groups and take the floor to get the nearest low int
    num_sensor_groups = ((last_channel - first_channel) + 1) / ch_group_size
    num_sensor_groups = math.floor(num_sensor_groups)
    #if not an even divide of total sensors by channel groups, add 1 to create one more channel group to include any remainder channels 
    if ((last_channel - first_channel) + 1) % ch_group_size != 0:
        num_sensor_groups += 1
    
    return num_sensor_groups

def calc_num_time_win(first_time_sample, last_time_sample, time_window):
    """
    Calculate the number of condensed time windows given a window size and number of time samples
    
    Number of time samples should be evenly divisible by the time window size.
    Time window size should be multiple of sampling frequency. 
    
    Parameters
    ----------
    first_time_sample : int
        Index of the first time sample in the data
    last_time_sample : int
        Index of the last time sample in the data
    time_window : int
        Number of time samples per window
    
    Returns
    -------
    int
        Number of time windows
    """
    
    #calculate the total number of time samples, add 1 since indexing starts 0 (last_time_sample - first_time_sample + 1)
    #divide by time window size to get number of windows (even divide)
    num_time_windows = ((last_time_sample - first_time_sample) + 1)  / time_window
    num_time_windows = int(num_time_windows)
    return num_time_windows


def calc_num_freq(n_time_samples, num_time_windows):
    """
    Calculate the number of resulting frequency bins given the number of time samples and number of time windows

    Parameters
    ----------
    n_time_samples : int
        Total number of time samples in data
    num_time_windows : int
        Number of time windows for data
    
    Returns
    -------
    int
        Number of frequency bins
    """
    
    #
    num_freq = int(n_time_samples / num_time_windows) + 1
    return num_freq


def condmatrix(some_data, num_time_windows, time_window, num_sensor_groups, ch_group_size, first_channel, last_channel, num_freq, nyq_freq):
    """
    Create and fill a 3D spectral tensor composed of condensed Fourier transformed data from an original 2D data array
    and calculate descriptive statistics (standard deviation, mean, maxiumums, peak frequency)
    
    3D tensor is created with shape (number of time windows, number of channel groups, number of frequency bins).
    Function iterates through slices of time samples and channels (time windows and channel groups) 
    from the original data and calculates, condenses and stores the discrete Fourier transform values 
    in the corresponding place in the spectral tensor.
    Outliers are determined using 1.5 times the interquartile range and removed. 
    
    Parameters
    ----------
    some_data : array
        2D array of original data read from file/data stream, with rows as time samples and columns as channels
    num_time_windows : int
        Number of time windows for data
    time_window : int
        Number of time samples per time window
    num_sensor_groups : int
        Number of channel groups for data
    ch_group_size : int
        Number of channels per channel group
    first_channel : int
        Index of first channel in data
    last_channel : int
        Index of last channel in data
    num_freq : int
        Number of frequency bins calculated from time samples and window size 
    nyq_freq : int
        Nyquist frequency of original data aka half of sampling frequency
    
    Returns
    -------
    tuple
        3D spectral tensor, 2D array of standard deviation values, 2D array of means for each window and channel group,
        1D array of max value for each channel, float of peak frequency having highest value 
    """
    
    #create spectral tensor 3D matrix
    spect = np.zeros((num_time_windows, num_sensor_groups, num_freq))
    
    
    #create 2D array to hold the std dev calculations for each ch group in time window
    std_devs = np.zeros((num_time_windows, num_sensor_groups))
    
    #create 2D array to hold the mean value for each ch group in time window
    means = np.zeros((num_time_windows, num_sensor_groups))
    
    #calculate the number of channels
    n_channels = last_channel - first_channel + 1
    #create 1D array to hold the max value for each channel
    max_vals = np.zeros(n_channels)
    
    #hold the peak frequency in hz
    peak_freq = 0.0
    #hold the value at the current peak frequency for comparison
    peak_freq_val = 0.0
    
    #iterate through n time windows
    for tw in range(num_time_windows):
        #iterate through n ch groups
        for ch in range(num_sensor_groups):
            #calculate index in original data matrix of beginning time sample of current time window
            windex = tw * time_window
            #calculate index in original matrix of beginning channel of current channel group
            cindex_beg = ch * ch_group_size
            #calculate index in original matrix of end channel of current channel group
            cindex_end = cindex_beg + ch_group_size
            
            #in case remainder channels due to noneven divide 
            if ch == (num_sensor_groups - 1):
                cindex_end = last_channel
            
            #get slice in matrix of original data for current time window and channel group
            data_slice = some_data[windex:(windex + time_window), cindex_beg:cindex_end]
            
            #take fft of slice of original data
            slice_fft = rfft(data_slice)
            
            #check for and get rid of outliers
            #take norms of columns to condense values for outlier check
            norm_slice = np.linalg.norm(slice_fft, axis=0)
            
            #use 1.5 * interquartile range as cutoff
            q1 = np.percentile(norm_slice, 25)
            q3 = np.percentile(norm_slice, 75)
            iqr = q3 - q1
            cutoff = 1.5 * iqr
            
            #check norm columns for outliers and record channel indexes 
            out_idxs = []
            for i in range(norm_slice.shape[0]):
                if (norm_slice[i] > (q3 + cutoff)) or (norm_slice[i] < (q1 - cutoff)):
                    out_idxs.append(i)
            
            #get non outlier array by deleting outlier channels
            trimmed_arr = np.delete(slice_fft, out_idxs, axis=1)
            
            #avg together channel groups, np.abs to get rid of complex parts created through fft
            absavgs = np.abs(np.mean(trimmed_arr, axis=1))

            #store in spect[window, group, all frequencies]
            spect[tw, ch, :] = absavgs
            
            #calculate and store mean of tw and ch group
            mean_slice = np.mean(slice_fft)
            
            means[tw, ch] = mean_slice
            
            #print(mean_slice)
            
            #calculate and store std dev
            num_channels = cindex_end - cindex_beg + 1
            num_observations = time_window * num_channels
            variance = (np.sum(np.square((slice_fft - mean_slice)))) / (num_observations - 1)
            stddev = np.sqrt(variance)
            
            std_devs[tw, ch] = stddev
            
            #print(np.std(slice_fft))
            
            #check and store max value for channels
            maximums = np.max(slice_fft, axis=0)
            for n in range(num_channels):
                if maximums[n] > max_vals[n + cindex_beg]:
                    max_vals[n + cindex_beg] = maximums[n]
            
            #check and store peak frequency 
            #add abs values along freq axis
            abs_sums = np.sum(slice_fft, axis=1)
            #get max freq index
            max_ind = np.argmax(abs_sums)
            if abs_sums[max_ind] > peak_freq_val : 
                #get and store corresponding freq
                peak_freq_val = abs_sums[max_ind]
                #calculate freq in hz
                size_freq_bin = nyq_freq / some_data.shape[0]
                freq_bin_idx = max_ind + windex
                peak_freq = freq_bin_idx * size_freq_bin
        
    return spect, std_devs, means, max_vals, peak_freq
    