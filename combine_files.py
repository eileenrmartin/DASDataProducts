from tdms_reader import TdmsReader
import condenser
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
import params


def main(file_paths):

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
    big_tens = np.zeros((num_time_windows, num_files*num_sensor_groups, num_cond_freqs))
    
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
        data_freq = condenser.fftfreq(fs, len(some_data))
        
        #calculate number of frequencies to store
        num_freq = condenser.calc_num_freq(data_freq, num_time_windows)
        
        #get condensed matrix
        spect = condenser.condmatrix(some_data, num_time_windows, params.time_window, num_sensor_groups, params.ch_group_size, params.last_channel, num_freq)
        
        #avg similar frequencies to get smaller number of freq bins and frequencies to store
        spect = spect.reshape(num_time_windows, num_sensor_groups, num_freq // params.bin_size, params.bin_size)
        spect = np.mean(spect, axis=-1)
        
        #store spect in tensor
        t_indx = num_time_windows
        c_indx = i * num_sensor_groups
        big_tens[0:t_indx, c_indx:c_indx+spect.shape[1], :] = spect
        
        #fft of data
        data_fft = np.abs(condenser.rfft(some_data))
        
        #store standard deviations of channels
        ch_stds[:, i] = np.std(data_fft, axis=0)
        
        #store max values of channels
        ch_maxs[:, i] = np.max(data_fft, axis=0)
        
        #store peak frequency
        #add abs values along freq axis
        abs_sums = np.sum(data_fft, axis=1)
        #get max freq index
        max_ind = np.argmax(abs_sums)
        #get and store corresponding freq
        peak_freqs[i] = data_freq[max_ind]
        
    
    #create indices arrays

    channel_inds = ch_ind_array(num_sensor_groups)
    time_inds = tw_ind_array(fs, num_files)
    freq_inds = freq_ind_array(nyq_freq, num_cond_freqs)
    
    n_files = np.zeros(1)
    n_files[0] = num_files
    
    
    #test plot
    clip = np.percentile(np.absolute(big_tens[:,:,10]),95)
    fig1 = plt.figure()
    img1 = plt.imshow(big_tens[:,:,10], vmin=0, vmax=clip)
    plt.colorbar()
    plt.show(block=True)
    
    #CHECK NEW DATA PRODUCTS AND ADD TO SAVE
    
    #write indices arrays, data products and tensor to file
    np.savez(comp_file, n_files=n_files, time_inds=time_inds, freq_inds=freq_inds, channel_inds=channel_inds, big_tens=big_tens)
    
    comp_file.close()



def ch_ind_array(num_sensor_groups):
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



def tw_ind_array(fs, num_files):
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