""" Data Products Files Reader

This script takes in the files of saved data products created by the 'save_data_prod.py' script and 
shows how to fetch the data and examples of how they can be plotted.

"""

import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    #path to save files to
    path = '../../writeup/'

    #get name of file to read from command line
    filename = sys.argv[1]
    
    #open data product file
    f = h5py.File(filename, 'r')
    
    #print list of attributes/metadata
    print(f.attrs.keys())
    
    #grab metadata values
    beg_time = f.attrs['first_sample_time']         #time of fetching data (year_month_day-hour_min_sec_timezone)
    tw_size = f.attrs['time_window_size']           #length of time window in seconds
    n_time_windows = f.attrs['num_time_windows']    #number of time windows      
    min_data = f.attrs['min_of_data_fetched']       #number of minutes of data fetched from server
    n_ch_groups = f.attrs['num_ch_groups']          #number of channel groups
    ch_group_size = f.attrs['ch_group_size']        #number of channels per group (except remainder channels group which is size : n_channels - ((num_sensor_groups - 1)*ch_group_size))
    n_channels = f.attrs['num_channels']            #number of channels
    n_freq_bin = f.attrs['num_freq_bins']           #number of frequency bins
    freq_bin_size = f.attrs['width_freq_bin']       #width of each freq bin in Hz
    nyq_freq = f.attrs['nyquist_freq']              #nyquist frequency 
    dt = f.attrs['dt']                              #dt value
    dx = f.attrs['dx']                              #dx value
    
    #print list of file keys
    print(list(f.keys()))
    
    #get spectral tensor dataset
    #note - datasets are specific to hdf5, may need to be cast to numpy array to use in other functions
    spect = f['spectral_tensor']
    
    #example plot of slice at one time window 
    clip = np.percentile(np.absolute(spect[0,:,:]),99.5)
    fig1 = plt.figure()
    img1 = plt.imshow(spect[0,:,:], aspect='auto', extent=(0, nyq_freq, n_ch_groups, 0), vmin=0, vmax=clip)
    plt.colorbar()
    plt.title('Spectral tensor : Time window 0')
    plt.ylabel('Channel group')
    plt.xlabel('Freq (Hz)')
    plt.savefig(path + 'file_tw0.png')
    
    
    
    #get time domain statistics 
    time_stats = f['time_domain_stats']
    #print list of datasets in time domain stats group
    print(list(time_stats.keys()))
    means_t = time_stats['means']
    std_devs_t = time_stats['std_deviations']
    maxs_t = time_stats['maximums']
    
    print(means_t.shape)
    #plot means of time domain
    fig2 = plt.figure()
    img2 = plt.plot(means_t[:])
    plt.title('Channel means (time)')
    plt.ylabel('Mean Intensity')
    plt.xlabel('Channel #')
    plt.savefig(path + 'file_meanst.png')
    
    #plot std of time domain
    fig2 = plt.figure()
    img2 = plt.plot(std_devs_t[:])
    plt.title('Channel std deviation (time)')
    plt.ylabel('Intensity')
    plt.xlabel('Channel #')
    plt.savefig(path + 'file_stdt.png')
    
    #plot maxs of time domain
    fig2 = plt.figure()
    img2 = plt.plot(maxs_t[:])
    plt.title('Channel maximums (time)')
    plt.ylabel('Intensity')
    plt.xlabel('Channel #')
    plt.savefig(path + 'file_maxt.png')
    
    #get freq domain statistics
    freq_stats = f['frequency_domain_stats']
    #print list of datasets in freq domain stats group
    print(list(freq_stats.keys()))
    means_f = freq_stats['means']
    std_devs_f = freq_stats['std_deviations']
    maxs_f = freq_stats['maximums']
    peak_freq = freq_stats['peak_frequency']
    
    #plot means of freq domain
    fig3 = plt.figure()
    img3 = plt.plot(means_f[:])
    plt.title('Channel means (freq)')
    plt.ylabel('Mean Intensity')
    plt.xlabel('Channel #')
    plt.savefig(path + 'file_meansf.png')

    #plot std of freq domain
    fig2 = plt.figure()
    img2 = plt.imshow(std_devs_f[:], aspect='auto')
    plt.title('Channel std deviation (freq)')
    plt.colorbar()
    plt.ylabel('Time window')
    plt.xlabel('Channel group')
    plt.savefig(path + 'file_stdf.png')
    
    #plot maxs of freq domain
    fig2 = plt.figure()
    img2 = plt.plot(maxs_f[:])
    plt.title('Channel maximums (freq)')
    plt.ylabel('Intensity')
    plt.xlabel('Channel #')
    plt.savefig(path + 'file_maxf.png')
    
    #peak freq
    print(peak_freq[()])
    
    
    #get lowpass and downsample data
    lpds = f['lowpass_downsample_signals']
    downsamp_time = lpds['downsample_time']
    downsamp_signal = lpds['lowpass_and_downsample']
    downsamp_freq = lpds['downsampled_sampling_freq']
    
    fig = plt.figure(figsize=(10,10))
    plt.plot(downsamp_time, downsamp_signal[channelNumber,:], 'r-', label='downsampled signal')
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.savefig(path + 'lowpassAndDownsampleFigure.png')
    plt.close()
    
    
