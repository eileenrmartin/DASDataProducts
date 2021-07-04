""" Combine Files Data Products

This script uses the condenser.py functions to create data products for individual files and save them together into 
a file. Indices arrays with information about time, channels, and frequency are also saved. When creating the 
individual spectral tensors similar frequency bins can also be further condensed. A params.py file is needed to 
define the condenser function parameters. A TDMSReader script (from Silixa) is used to read in original DAS data. 

Functions
---------
main - Main function to create bigger tensor and indices arrays and save to file
ch_ind_array - Create the channel info array
tw_ind_array - Create the time info array
freq_ind_array - Create the frequency info array

"""

from tdms_reader import TdmsReader
import condenser
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
import params
import time


def main(file_paths):
    """
    Main function to create a bigger 3D spectral tensor from individual spectral tensors from data 
    from individual files. The big tensor and indices arrays are saved to a file for the user. 
    
    Parameters
    ----------
    file_paths : list of strings
        Strings of filenames of DAS tdms data files to analyze
    """

    #create new file to write compressed data to (change name format for diff file sets?)
    comp_file = open("compdata", "wb")
    
    #number of files to combine
    num_files = len(file_paths)
     
    #get number of sensor groups and time windows
    num_sensor_groups = condenser.calc_num_ch_groups(params.first_channel, params.last_channel, params.ch_group_size)
    num_time_windows = condenser.calc_num_time_win(params.first_time_sample, params.last_time_sample,params.time_window)
    
    fs = 500    #sampling frequency, for now assume constant, read from file
    nyq_freq = fs / 2   #nyquist freq
    
    #to combine in one big tensor, store created spect arrays
    #change freqs, pare down to smaller avgs
    num_cond_freqs = int(((params.time_window / 2) + 1) / params.bin_size)
    
    #create big tensor to hold all spectra
    #params same for each file, so tensor bigger lengthwise
    #check num freq param is same as time window size
    big_tens = np.zeros((num_files*num_time_windows, num_sensor_groups, num_cond_freqs))
    
    #data products
    
    #standard deviations for channels per each file
    n_channels = params.last_channel - params.first_channel + 1
    ch_stds = np.zeros((n_channels, num_files))
    
    #max value for each channel per file
    ch_maxs = np.zeros((n_channels, num_files))
    
    #peak frequency per file
    peak_freqs = np.zeros(num_files)
    
    
    #write each of files to cond file
    for i in range(len(file_paths)):
        #pull file from list
        fp = file_paths[i]
        
        #get tdms reader
        tdms = TdmsReader(fp)
        #read in tdms data - array of time samples x channels
        some_data = tdms.get_data(params.first_channel, params.last_channel, params.first_time_sample, params.last_time_sample)
        
        #get fourier corresponding frequency values
        #after testing peak freq, not needed
        data_freq = condenser.fftfreq(fs, len(some_data))
        
        #calculate number of frequencies to store
        num_freq = condenser.calc_num_freq(len(some_data), num_time_windows)
        
        t0 = time.time()
        
        #get condensed matrix
        spect, std_devs, means, max_vals, peak_freq = condenser.condmatrix(some_data, num_time_windows, params.time_window, num_sensor_groups, params.ch_group_size, params.first_channel, params.last_channel, num_freq, nyq_freq)
        
        t1 = time.time()
        print('time to create cond matrix: {0}'.format(t1-t0))
        
        
        #avg similar frequencies to get smaller number of freq bins and frequencies to store
        spect = spect.reshape(num_time_windows, num_sensor_groups, num_freq // params.bin_size, params.bin_size)
        spect = np.mean(spect, axis=-1)
        
        t2 = time.time()
        print('time to bin similar freq: {0}'.format(t2-t1))
        
        
        #store spect in tensor
        t_indx = i * num_time_windows
        c_indx = num_sensor_groups
        big_tens[t_indx:t_indx+spect.shape[0], 0:c_indx, :] = spect
        
        #fft of data
        data_fft = np.abs(condenser.rfft(some_data))
        
        #store standard deviations of channels
        #ch_stds[:, i] = np.std(data_fft, axis=0)
        
        #store max values of channels
        ch_maxs[:, i] = np.max(data_fft, axis=0)
        print(ch_maxs[:, i])
        
        #store peak frequency
        #add abs values along freq axis
        abs_sums = np.sum(data_fft, axis=1)
        #get max freq index
        max_ind = np.argmax(abs_sums)
        #get and store corresponding freq
        peak_freqs[i] = data_freq[max_ind]
        print(max_ind)
        print(peak_freqs[i])
    
    #create indices arrays

    t3 = time.time()
    
    channel_inds = ch_ind_array(num_sensor_groups)
    
    t4 = time.time()
    print('time to create ch ind array: {0}'.format(t4-t3))
    
    
    time_inds = tw_ind_array(fs, num_files)
    
    t5 = time.time()
    print('time to create time ind array: {0}'.format(t5-t4))
    
    freq_inds = freq_ind_array(nyq_freq, num_cond_freqs)
    
    t6 = time.time()
    print('time to create freq ind array: {0}'.format(t6-t5))
    
    
    n_files = np.zeros(1)
    n_files[0] = num_files
    
    
    #test plot
    clip = np.percentile(np.absolute(big_tens[:,:,10]),95)
    fig1 = plt.figure()
    img1 = plt.imshow(big_tens[:,:,10], vmin=0, vmax=clip, aspect='auto')
    plt.colorbar()
    plt.title('4/26/19 20:54-58')
    plt.ylabel('Time Window')
    plt.xlabel('Channel Group')
    plt.show(block=True)
    
    #CHECK NEW DATA PRODUCTS AND ADD TO SAVE
    
    #write indices arrays, data products and tensor to file
    np.savez(comp_file, n_files=n_files, time_inds=time_inds, freq_inds=freq_inds, channel_inds=channel_inds, big_tens=big_tens)
    
    comp_file.close()



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
        start_channel = k * params.ch_group_size
        end_channel = start_channel + params.ch_group_size - 1
        #check for if channel groups not divisible
        if k == (num_sensor_groups - 1):
            end_channel = params.last_channel
        channel_inds[2*k + 1] = start_channel   
        channel_inds[2*k + 2] = end_channel
    
    return channel_inds


#CHANGE SECONDS TO MILISEC TO COMPENSATE FOR TW SIZE NOT AN EVEN NUM OF SEC
def tw_ind_array(fs, num_files):
    """
    Create the array to hold information about time, including the length of each time window in 
    seconds and datetime objects holding the starting time in UTC for the start of each time window
    
    Parameters
    ----------
    fs : int
        Sampling frequency of original data
    num_files : int
        Number of files to combine
    
    Returns
    -------
    array
        Time information
    """
    
    #create 1d array to hold time information
    time_inds = []
    
    #add time info to time window indices array
    wind_length = int(params.time_window / fs)    #length of window in secs
    time_inds.append(wind_length)
    #add datetime objs of UTC start time of windows
    start_hour = params.file_hour_start
    start_min = params.file_min_start
    #start datetime obj of first file
    start_dttime = datetime(params.file_year, params.file_month, params.file_day, start_hour, start_min, 0, tzinfo=pytz.UTC)   
    total_seconds = num_files * 60        #total number of seconds in all files
    
    #add datetime start time for each time window
    for j in range(0, total_seconds, wind_length):
        time_inds.append(start_dttime + timedelta(seconds=j))
    
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



if __name__ == '__main__':
    print("Condensing files attempt")
    
    #file path names
    file_paths = []
    
    #find time difference in file range
    hour_diff = params.file_hour_end - params.file_hour_start
    min_diff = 0
    if params.file_min_end > params.file_min_start:
        min_diff = params.file_min_end - params.file_min_start
    else:
        hour_diff = hour_diff - 1
        min_diff = (params.file_min_end + 60) - params.file_min_start

    #calc number of files
    n_files = (hour_diff * 60) + min_diff + 1 

    hour_count = params.file_hour_start
    min_count = params.file_min_start

    for i in range(n_files):
        #add filename to list of files
        name = 'PSUDAS_UTC_' + str(params.file_year) + '{:02}'.format(params.file_month) + '{:02}'.format(params.file_day) + '_' + '{:02}'.format(hour_count) + '{:02}'.format(min_count) + '43.415.tdms'
        file_paths.append(name)
        #increment minutes and hour if applicable
        if min_count < 59:
            min_count = min_count + 1 
        else:
            min_count = 0
            hour_count = hour_count + 1
    
    main(file_paths)