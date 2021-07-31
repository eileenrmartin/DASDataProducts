""" Combine Files Data Products

This is the main script for calculating and combining data products for multiple tdms files. It uses 
the condenser.py and tdms_func.py functions to create data products for individual tdms files and save 
them together into a single file. Indices arrays with information about time, channels, and frequency 
are also saved. A tdms_params.py file is needed to define the condenser function parameters.

Functions
---------
main - Main function to create bigger tensor and indices arrays and save to file

"""
import sys
sys.path.insert(1, '..')
import condenser
import numpy as np
import matplotlib.pyplot as plt
import tdms_params as tp
import tdms_func

    

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
    num_sensor_groups = condenser.calc_num_ch_groups(tp.first_channel, tp.last_channel, tp.ch_group_size)
    num_time_windows = condenser.calc_num_time_win(tp.first_time_sample, tp.last_time_sample, tp.time_window)
    
    nyq_freq = tp.fs / 2   #nyquist freq
    
    #change freqs, pare down to smaller avgs
    num_cond_freqs = int(((tp.time_window / 2) + 1) / tp.bin_size)
    
    #get bigger tensor and stats arrays
    big_tens, ch_stds, ch_means, ch_maxs, peak_freqs = tdms_func.combine_data_products(num_files, num_time_windows, num_sensor_groups, num_cond_freqs, file_paths, nyq_freq)
    
    #create indices arrays
    channel_inds = tdms_func.ch_ind_array(num_sensor_groups)
    
    time_inds = tdms_func.tw_ind_array(tp.fs, num_files)
    
    freq_inds = tdms_func.freq_ind_array(nyq_freq, num_cond_freqs)
    
    #store number of files 
    n_files = np.zeros(1)
    n_files[0] = num_files
    
    #test plot - move to test/example scrpit
    clip = np.percentile(np.absolute(big_tens[:,:,10]),95)
    fig1 = plt.figure()
    img1 = plt.imshow(big_tens[:,:,10], vmin=0, vmax=clip, aspect='auto')
    plt.colorbar()
    plt.title('4/26/19 20:54-58')
    plt.ylabel('Time Window')
    plt.xlabel('Channel Group')
    plt.savefig("data.png")
    
    #write indices arrays, data products and tensor to file
    np.savez(comp_file, n_files=n_files, time_inds=time_inds, freq_inds=freq_inds, channel_inds=channel_inds, big_tens=big_tens, 
        ch_stds=ch_stds, ch_means=ch_means, ch_maxs=ch_maxs, peak_freqs=peak_freqs)
    
    comp_file.close()


if __name__ == '__main__':
    print("Condensing files attempt")
    
    file_paths = tdms_func.create_file_names()
    
    #value checks
    num_time_samples = (tp.last_time_sample - tp.first_time_sample) + 1
    
    #check if time window size is multiple of sampling freq and divides evenly number of samples
    if (num_time_samples % tp.time_window) != 0:
        print("Warning! Time window size does not evenly divide the number of time samples in original data")
    if (tp.time_window % tp.fs) != 0:
        print("Warning! Time window size is not evenly divided by the sampling frequency")
    
    main(file_paths)