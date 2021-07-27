""" Save Data Products From Stream

This script is meant to be called repeatedly to continuously fetch data from a treble server 
and calculate and store data products in a file. 

"""

from T15 import treble_setup
#from acq_common import acq_client
import condenser
import numpy as np
import matplotlib.pyplot as plt
import params
import time


#def t15_attempt():
    
    #dt not even - fix everything - changes sampling freq, nyq freq
    #time window size must be either number of frames or number of time samples per frame
    
    
import h5py

if __name__ == '__main__':
    t0 = time.time()
    print("Fetch data from server attempt")
    
    #value checks
    #num_time_samples = (params.last_time_sample - params.first_time_sample) + 1
    
    #check if time window size is multiple of sampling freq and divides evenly number of samples
    #if (num_time_samples % params.time_window) != 0:
    #    print("Warning! Time window size does not evenly divide the number of time samples in original data")
    #if (params.time_window % params.fs) != 0:
    #    print("Warning! Time window size is not evenly divided by the sampling frequency")
    
    #set up connection to server
    #client = treble_setup.setup_server()
    
    #setup_params = client.fetch_setup_parm()
    
    n_frames = 140
    
    #get a min of reshaped data (2D, time samples by channels)
    #output, md = treble_setup.get_data(client, n_frames)
    #print(output.shape)
    #print(md)

    #calculate number of time windows
    #time_window = md['nT']
    #num_time_windows = condenser.calc_num_time_win(0, output.shape[0], time_window)
    
    #ch_group_size = 100
    
    #calculate number of channel groups
    #num_sensor_groups = condenser.calc_num_ch_groups(0, output.shape[1], ch_group_size)
    
    #calculate number of frequencies to store
    #num_freq = condenser.calc_num_freq(len(output), num_time_windows)
    
    #dT value from md, used to calculate nyquist
    #nyq_freq = condenser.calc_nyq_freq(md['dT'])
    
    filename = 'Kafadar_Coupling_deformation_UTC-YMD20201202-HMS174339.516_seq_00000000000.hdf5'

    f = h5py.File(filename, 'r')
    print(list(f['deformation/frame_'+str(0).zfill(10)].attrs))
    print(f['deformation/frame_'+str(0).zfill(10)].attrs['nx'])
    print(f['deformation/frame_'+str(0).zfill(10)].attrs['dT'])
    # slices data
    deformframes = f['deformation/frame_'+str(0).zfill(10)][:,:]

    for k in range(1,n_frames):
        deformation_frame = f['deformation/frame_'+str(k).zfill(10)][:,:]
        deformframes = np.concatenate([deformframes, deformation_frame],axis=0)
    
    print(deformframes.shape)
    num_time_windows = n_frames
    time_window = 714
    num_sensor_groups = 9
    ch_group_size = 100
    first_channel = 0
    last_channel = 815
    num_freq =  condenser.calc_num_freq(len(deformframes), num_time_windows)
    nyq_freq = condenser.calc_nyq_freq(0.00022384)
    
    
    #get condensed matrix
    spect, std_devs, means, max_vals, peak_freq = condenser.condmatrix(deformframes, num_time_windows, time_window, num_sensor_groups, ch_group_size, first_channel, last_channel, num_freq, nyq_freq)
    print(time.time() - t0)