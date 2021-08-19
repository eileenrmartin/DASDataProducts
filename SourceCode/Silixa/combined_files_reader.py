#ADD DOCUMENTATION COMMENTS AND EXPLANATIONS


import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    #get filename from command line
    filename = "compdata"
    
    #load combined data file
    npzfile = np.load(filename, allow_pickle=True)
    
    #get number of files
    n_files = npzfile['n_files']
    num_files = n_files[0]              #number of files
    
    #get time info array
    time_inds = npzfile['time_inds'] 
    window_len = time_inds[0]           #length of time windows in seconds
    num_time_windows = time_inds[1]     #number of time windows
    
    #datetime object for the start time of each time window
    for i in range(2, len(time_inds)):
        datetime_start_tw = time_inds[i]
        #print(datetime_start_tw)
    
    #get frequency info array
    freq_inds = npzfile['freq_inds'] 
    num_cond_freqs = freq_inds[0]            #number of freq bins
    width_freq_bins = freq_inds[1]          #width of freq bins in Hz
    nyq_freq = freq_inds[2]                #nyquist frequency in Hz
    
    #get channel info array
    channel_inds = npzfile['channel_inds'] 
    num_sensor_groups = channel_inds[0]       #number of channel groups in a single file (same for all files)
    
    #start and end indices of channels in each channel group, same for all files 
    #(ex. for channel group size 100, ch group 0 has start indices 0 and end indices 99, followed by ch group 1 with indices 100 and 199...)
    for j in range(int(num_sensor_groups)):
        #ch_group_number = j
        start_ind_of_group = channel_inds[2*j + 1]
        end_ind_of_group = channel_inds[2*j + 2]
        #print(start_ind_of_group)
    
    #get big tensor containing series of file spectra
    #big tensor is 3d tensor of size    (number of files*number of time windows) * (number of channel groups) * (number of freq bins)
    big_tens = npzfile['big_tens'] 
    
    #get 3d spectra array for each file
    for k in range(int(num_files)):
        t_indx = k * int(num_time_windows)
        #get spectra array for kth file in big tensor
        spect = big_tens[t_indx:t_indx+int(num_time_windows), :, :]
        
        #plot one ch group
        #cond_data = spect[:, 22, :]
        
        #fig5 = plt.figure()
        #img5 = plt.imshow(cond_data, aspect='auto', interpolation='none')
        #plt.colorbar()
        #plt.ylabel('Time window (len of 1000 frames)')
        #plt.xlabel('Frequency (Hz)')
        #plt.show(block=True)
    
    #test plot
    clip = np.percentile(np.absolute(big_tens[:,:,10]),95)
    fig1 = plt.figure()
    img1 = plt.imshow(big_tens[:,:,10], vmin=0, vmax=clip)
    plt.colorbar()
    plt.show(block=True)
    
    #get statistics arrays for files
    ch_stds = npzfile['ch_stds']
    #get std deviations for each file
    for l in range(int(num_files)):
        #std deviations for each file are for each time window and channel group
        file_stds = ch_stds[l, :, :]
        #get std dev for a time window and channel group
        tw = 10
        ch = 10
        tw_ch_std = file_stds[tw, ch]

    ch_means = npzfile['ch_means']
    for m in range(int(num_files)):
        #means for each file are a mean value for each channel
        file_means = ch_means[m, :]
    
    ch_maxs = npzfile['ch_maxs']
    for n in range(int(num_files)):
        #maxs for each file are a maximum value for each channel
        file_maxs = ch_maxs[n, :]
    
    peak_freqs = npzfile['peak_freqs']
    for p in range(int(num_files)):
        #peak freq for each file is the frequency with the maximum intensity value
        file_freq = peak_freqs[p]