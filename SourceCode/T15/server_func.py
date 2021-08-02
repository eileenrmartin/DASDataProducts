""" Treble Server Setup

This module contains functions necessary for setting up the connection to the 
treble server. Using the connected client, frames of data can be fetched as it 
is being recorded. The .whl for the treble must be downloaded so the acq_client 
module can use the treble api functions. 

Functions
---------
setup_server - sets up connection to the local server
get_data - fetches a number of frames from data stream
save_file - Calculates data products and saves to file
"""

from acq_common import acq_client
import condenser
import numpy as np
import time
import h5py


def setup_server():
    """
    Sets up client connection to treble server 
    
    Returns
    -------
    object
        Client connected to the local computer host
    """
    
    client = acq_client.acq_Client()
    client.connect_to_server("tcp://localhost:50000")
    
    return client

def get_data(client, n_frames):
    """
    Fetches a specified number of frames of data from the client connected to a 
    server. The fetched data comes in shape ((n_frames, number time samples, number channels)).
    The 3D data is then reshaped to a 2D array, of shape ((n_frames * number time samples, number channels)).
    
    Parameters
    ----------
    client : object
        Client object connected to server
    n_frames : int
        Number of data frames to fetch
    
    Returns
    -------
    array
        2D data fetched from data stream
    """
    
    data, md = client.fetch_data_product(list(range(-n_frames+1, 1)))
    output = data.reshape(-1, data.shape[2])
    
    return output, md


def save_file(filename):
    """
    Calculates the data products and statistics for the fetched data, then
    save them to a file in hdf5 format. 
    
    Parameters
    ----------
    filename : string
        Name of parameter file
    """
    
    fp = open(filename, "r")
    #read first three lines (explanatory info)
    lines = [line.rstrip() for line in fp]
    
    ch_group_size = int(lines[3])   #number of channels in each ch group
    tw_frames = int(lines[4])     #number of frames in each time window
    file_path = lines[5]
    
    fp.close()
    
    #set up connection to server
    client = setup_server()
    
    #fetch one frame to get metadata values
    output, md = get_data(client, 1)
    print(output.shape)
    print(md)
    
    samp_per_frame = md['nT']       #number of time samples per frame
    n_channels = md['nx']           #number of channels
    dx = md['dx']                   #spacing between channels (m)
    dt = md['dT']                   #spacing between time samples (sec)
    
    #calc time window size (number of samples)
    time_window = tw_frames * samp_per_frame
    
    #calc sampling rate
    samp_rate = 1 / dt
    
    #determine number of frames to fetch from dt
    #seconds * samples/sec * frame/samples
    n_frames = int(60 * samp_rate * (1 / samp_per_frame))
    #add few frames to account for fetching md?
    
    #get a minute of reshaped data (2D, time samples by channels)
    
    #output, md = get_data(client, n_frames)
    output, md = get_data(client, 140)

    num_time_samples = output.shape[0]

    #size of time window
    #num of time samples per tw must be div by 2
    
    #value checks
    
    #check if tw_frames size divides evenly number of frames
    #if (num_time_samples % time_window) != 0:
    #    print("Warning! Time window size does not evenly divide the number of time samples in original data")

    #calculate number of time windows
    first_time_sample = 0
    num_time_windows = condenser.calc_num_time_win(first_time_sample, num_time_samples - 1, time_window)
    
    #calculate number of channel groups
    first_channel = 0
    last_channel = n_channels - 1
    num_sensor_groups = condenser.calc_num_ch_groups(first_channel, last_channel, ch_group_size)
    
    #calculate number of frequencies to store
    num_freq = condenser.calc_num_freq(num_time_samples, num_time_windows)
    
    #dT value from md, used to calculate nyquist
    nyq_freq = condenser.calc_nyq_freq(dt)
    
    #get condensed matrix and frequency domain stats
    spect, std_devs, means, max_vals, peak_freq = condenser.condmatrix(output, num_time_windows, time_window, num_sensor_groups, ch_group_size, first_channel, last_channel, num_freq, nyq_freq)
    
    #get time domain stats
    means_t = condenser.mean_time(output)
    stds_t = condenser.std_dev_time(output)
    maxs_t = condenser.max_time(output)
    
    #save as hdf5 file
    
    #create filename using path to save file and current time
    save_name = file_path + '/DataProducts_' + time.strftime("%Y_%m_%d-%H_%M_%S_%Z") + '.hdf5'
    hf = h5py.File(save_name, 'w')
    
    hf.create_dataset('spectral_tensor', data=spect)
    
    freq_g = hf.create_group('frequency_domain_stats')
    freq_g.create_dataset('std_deviations',data=std_devs)
    freq_g.create_dataset('means',data=means)
    freq_g.create_dataset('maximums',data=max_vals)
    freq_g.create_dataset('peak_frequency',data=peak_freq)
    
    time_g = hf.create_group('time_domain_stats')
    time_g.create_dataset('std_deviations',data=stds_t)
    time_g.create_dataset('means',data=means_t)
    time_g.create_dataset('maximums',data=maxs_t)
    
    #save metadata
    #hf.attrs['first_sample_time'] = 0.01                       #time of the first time sample
    hf.attrs['time_window_size'] = time_window * dt             #length of time window in seconds
    hf.attrs['num_time_windows'] = num_time_windows             #number of time windows      
    hf.attrs['num_ch_groups'] = num_sensor_groups               #number of channel groups
    hf.attrs['num_channels'] = n_channels                       #number of channels
    hf.attrs['num_freq_bins'] = num_freq                        #number of frequency bins
    hf.attrs['width_freq_bin'] = nyq_freq / num_freq            #width of each freq bin in Hz
    hf.attrs['nyquist_freq'] = nyq_freq                         #nyquist frequency 
    hf.attrs['dt'] = dt                                         #dt value
    hf.attrs['dx'] = dx                                         #dx value
    
    hf.close()