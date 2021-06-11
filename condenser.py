import numpy as np
from scipy import fft
from scipy import stats
import math


def rfft(some_data):
    # fourier transform of array some_data
    data_fft = fft.rfft2(some_data, axes=-2)
    return data_fft


def fftfreq(fs, n_time):
    # frequency bins
    #fftfreq(num samples, sampling freq) -> num samples is len(some_data)
    data_freq = fft.rfftfreq(n_time, d=(1./fs))
    return data_freq


def calc_num_ch_groups(first_channel, last_channel, ch_group_size):
    #find actual indexes of channels (so n_channels/gsize works), add 1 since index starts 0
    num_sensor_groups = ((last_channel - first_channel) + 1) / ch_group_size
    num_sensor_groups = math.floor(num_sensor_groups)
    #if not an even divide of total sensors by channel groups, add 1 to iterate over remainder channels 
    if ((last_channel - first_channel) + 1) % ch_group_size != 0:
        num_sensor_groups += 1
    
    return num_sensor_groups


def calc_num_time_win(first_time_sample, last_time_sample, time_window):
    #for now assume even divide with 500 - makes datetime seconds friendly
    num_time_windows = ((last_time_sample - first_time_sample) + 1)  / time_window
    num_time_windows = int(num_time_windows)
    return num_time_windows


def calc_num_freq(data_freq, num_time_windows):
    num_freq = int(len(data_freq) / num_time_windows) + 1
    return num_freq


def condmatrix(some_data, num_time_windows, time_window, num_sensor_groups, ch_group_size, last_channel, num_freq):
    
    #create smaller matrix
    spect = np.zeros((num_time_windows, num_sensor_groups, num_freq))
    
    #run through n time windows
    for tw in range(num_time_windows):
        #run through n ch groups
        for ch in range(num_sensor_groups):
            #get slice in large matrix (timewindow, channels, axis = time axis)
            windex = tw * time_window
            cindex_beg = ch * ch_group_size
            cindex_end = cindex_beg + ch_group_size
            
            #in case remainder channels due to noneven divide 
            if ch == (num_sensor_groups - 1):
                cindex_end = last_channel
            
            #take orig matrix
            data_slice = some_data[windex:(windex + time_window), cindex_beg:cindex_end]
            
            #take fft of slice of orig data
            slice_fft = rfft(data_slice)
            
            #check for and get rid of outliers
            #take norms of columns to condense values for outlier check
            norm_slice = np.linalg.norm(slice_fft, axis=0)
            
            #use 1.5 * interquartile range as cutoff
            q1 = np.percentile(norm_slice, 25)
            q3 = np.percentile(norm_slice, 75)
            iqr = q3 - q1
            cutoff = 1.5 * iqr
            
            #check norm columns for outliers
            out_idxs = []
            for i in range(norm_slice.shape[0]):
                if (norm_slice[i] > (q3 + cutoff)) or (norm_slice[i] < (q1 - cutoff)):
                    out_idxs.append(i)
            
            #get non outlier array 
            trimmed_arr = np.delete(slice_fft, out_idxs, axis=1)
            
            #avg together channel groups, np.abs
            absavgs = np.abs(np.mean(trimmed_arr, axis=1))

            #store in spect[window, groups, :]
            spect[tw, ch, :] = absavgs
    
    return spect
    
def stddev_spect(spect):
    #get standard deviation of 3d spectral tensor
    return np.std(spect)
    
def stddev_ch(spect):
    #get standard deviation of channel groups in tensor
    
    #num of ch groups in tensor
    n_groups = spect.shape[1]
    
    ch_stds = np.zeros(n_groups)
    for ch in range(n_groups):
        ch_slice = spect[:, ch, :]
        ch_stds[ch] = np.std(ch_slice)
    
    return ch_stds