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
import math
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
    
    #check if successfully fetched data - otherwise data is nonetype
    if data is None:
        print("Warning : Data not fetched from server")
    
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
    
    #get variables from params file from command line
    module = __import__(filename.replace('.py', ''))
    
    ch_group_size = module.ch_group_size
    min_data = module.min_data
    file_path = module.file_path
    
    #set up connection to server
    client = setup_server()
    
    #fetch one frame to get metadata values
    output, md = get_data(client, 1)
    
    print(md)
    
    samp_per_frame = md['nT']       #number of time samples per frame
    n_channels = md['nx']           #number of channels
    dx = md['dx']                   #spacing between channels (m)
    dt = md['dT']                   #spacing between time samples (sec)
    
    #calc sampling rate
    samp_rate = 1 / dt
    
    #determine number of frames to fetch from dt
    #seconds * samples/sec * frame/samples
    n_frames = math.ceil(min_data * 60 * samp_rate * (1 / samp_per_frame))
    
    #check in case n_frames calc is bigger than buffer - testing computer buffer holds max 140 frames
    n_frames = min(n_frames, 140)
    
    #set time window size (number of samples) so evenly divisible
    time_window = samp_per_frame
    
    #get time of grabbing data
    beg_time = time.strftime("%Y_%m_%d-%H_%M_%S_%Z")
    #get a minute of reshaped data (2D, time samples by channels)
    output, md = get_data(client, n_frames)

    #number of time samples in fetched data
    num_time_samples = output.shape[0]

    #calculate number of time windows
    num_time_windows = condenser.calc_num_time_win(num_time_samples, time_window)
    
    #calculate number of channel groups
    num_sensor_groups = condenser.calc_num_ch_groups(n_channels, ch_group_size)
    
    #calculate number of frequencies to store
    num_freq = condenser.calc_num_freq(num_time_samples, num_time_windows)
    
    #dT value from md, used to calculate nyquist
    nyq_freq = condenser.calc_nyq_freq(dt)
    
    #get condensed matrix and frequency domain stats
    spect, std_devs, means, max_vals, peak_freq = condenser.condmatrix(output, num_time_windows, time_window, num_sensor_groups, ch_group_size, n_channels - 1, num_freq, nyq_freq)
    
    #avg together every 10 time windows to get smaller number of values to store, pad if number of tws are not evenly divided by 10
    spect = np.pad(spect.astype(float), ((0, 0 if spect.shape[0] % 10 == 0 else 10 - spect.shape[0] % 10), (0,0), (0,0)), mode='constant', constant_values=np.NaN)
    spect = spect.reshape(-1, 10, num_sensor_groups, num_freq)
    spect = np.nanmean(spect, axis=1)
    
    #get time domain stats
    means_t = condenser.mean_time(output)
    stds_t = condenser.std_dev_time(output)
    maxs_t = condenser.max_time(output)
    
    #save as hdf5 file
    
    #create filename using path to save file and time at fetching data
    save_name = file_path + '/DataProducts_' + beg_time + '.hdf5'
    hf = h5py.File(save_name, 'w')
    
    #save spectral tensor as a dataset
    hf.create_dataset('spectral_tensor', data=spect)
    
    #save frequency domain stats in a group
    freq_g = hf.create_group('frequency_domain_stats')
    freq_g.create_dataset('std_deviations',data=std_devs)
    freq_g.create_dataset('means',data=means)
    freq_g.create_dataset('maximums',data=max_vals)
    freq_g.create_dataset('peak_frequency',data=peak_freq)
    
    #save time domain stats in a group
    time_g = hf.create_group('time_domain_stats')
    time_g.create_dataset('std_deviations',data=stds_t)
    time_g.create_dataset('means',data=means_t)
    time_g.create_dataset('maximums',data=maxs_t)
    
    #save metadata
    hf.attrs['first_sample_time'] = beg_time                    #time of fetching data
    hf.attrs['time_window_size'] = time_window * dt             #length of time window in seconds
    hf.attrs['num_time_windows'] = num_time_windows             #number of time windows      
    hf.attrs['min_of_data_fetched'] = min_data                  #number of minutes of data fetched from server
    hf.attrs['num_ch_groups'] = num_sensor_groups               #number of channel groups
    hf.attrs['ch_group_size'] = ch_group_size                   #number of channels per group (except remainder channels group which is size : n_channels - ((num_sensor_groups - 1)*ch_group_size))
    hf.attrs['num_channels'] = n_channels                       #number of channels
    hf.attrs['num_freq_bins'] = num_freq                        #number of frequency bins
    hf.attrs['width_freq_bin'] = nyq_freq / num_freq            #width of each freq bin in Hz
    hf.attrs['nyquist_freq'] = nyq_freq                         #nyquist frequency 
    hf.attrs['dt'] = dt                                         #dt value
    hf.attrs['dx'] = dx                                         #dx value
    
    hf.close()