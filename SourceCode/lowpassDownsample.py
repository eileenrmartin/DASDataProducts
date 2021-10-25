import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from T15 import server_func
import condenser
from scipy.signal import iirfilter, zpk2sos, sosfilt, decimate
import warnings
from scipy.fft import rfft, rfftfreq
import sys
import time
import h5py
plt.switch_backend('agg')


def runLowpassOnly(integerDownsampleFactor, filterOrder):
    
    client = server_func.setup_server();
    data, md = server_func.get_data(client,1);
    #cutoff_freq = cutoffFrequency;
    dT = md['dT'];
    sampling_freq = 1/dT;
    nyquist_freq = sampling_freq/2;
    cutoff_freq = (int) (nyquist_freq/integerDownsampleFactor);
    #print(cutoff_freq, file=sys.stderr);
    data_T = np.transpose(data);
    lowpassData = lowpass(data_T, cutoff_freq, sampling_freq, filterOrder, zerophase=True);
    number_of_time_samples = md['nT'];
    sampling_duration = number_of_time_samples * dT;
    time = np.linspace(0, sampling_duration, number_of_time_samples, endpoint=False);
    #downsampled_data = lowpassData[::integerDownsampleFactor);
    #downsampled_data = scipy.signal.decimate(lowpassData,integerDownsampleFactor,n=filterOrder);
    print(cutoff_freq, file=sys.stderr);
    return (time, data_T, lowpassData,number_of_time_samples,sampling_duration,sampling_freq)
    
def runLp(integerDownsampleFactor, filterOrder, dT, data, number_of_time_samples):
    sampling_freq = 1/dT;
    nyquist_freq = sampling_freq/2;
    cutoff_freq = (int) (nyquist_freq/integerDownsampleFactor);
    data_T = np.transpose(data);
    lowpassData = lowpass(data_T, cutoff_freq, sampling_freq, filterOrder, zerophase=True);
    sampling_duration = number_of_time_samples * dT;
    time = np.linspace(0, sampling_duration, number_of_time_samples, endpoint=False);
    return (time, data_T, lowpassData,number_of_time_samples,sampling_duration,sampling_freq)


def runLowpassAndDownsample(integerDownsampleFactor):
    client = server_func.setup_server();
    data, md = server_func.get_data(client,1);
    dT = md['dT'];
    sampling_freq = 1/dT;
    data_T = np.transpose(data);
    number_of_time_samples = md['nT'];
    sampling_duration = number_of_time_samples * dT;
    time = np.linspace(0, sampling_duration, number_of_time_samples, endpoint=False);
    downsampled_signal = scipy.signal.decimate(data,integerDownsampleFactor);
    newNumSamples = len(downsampled_signal[0]);
    downsampled_time = np.linspace(0,sampling_duration,newNumSamples, endpoint=False);
    return (time,data_T,downsampled_time, downsampled_signal,sampling_freq)
    
def runLpAndDs(data, dT, sampling_freq, number_of_time_samples, integerDownsampleFactor):
    data_T = np.transpose(data);
    sampling_duration = number_of_time_samples * dT;
    time = np.linspace(0, sampling_duration, number_of_time_samples, endpoint=False);
    downsampled_signal = scipy.signal.decimate(data,integerDownsampleFactor);
    newNumSamples = len(downsampled_signal[0]);
    downsampled_time = np.linspace(0,sampling_duration,newNumSamples, endpoint=False);
    return (time,data_T,downsampled_time, downsampled_signal,sampling_freq)

def runLowpassAndDownsampleWithFile(integerDownsampleFactor, fileName):
    f = h5py.File(fileName, 'r')
    #print list of attributes/metadata
    #print(f.attrs.keys())
    #print(f.keys())
    group = f['data_product']
    data = group['data'][()]
    #print(data.shape)
    dT = f.attrs['dt_computer']
    #print(dT)
    number_of_time_samples = f.attrs['nt']
    #print(nT)
    sampling_freq = 1/dT;
    downsampled_sampling_freq = sampling_freq/integerDownsampleFactor
    #print(sampling_freq)
    data_T = np.transpose(data)
    sampling_duration = number_of_time_samples * dT;
    time = np.linspace(0, sampling_duration, number_of_time_samples, endpoint=False);
    downsampled_signal = scipy.signal.decimate(data_T,integerDownsampleFactor);
    newNumSamples = len(downsampled_signal[0]);
    downsampled_time = np.linspace(0,sampling_duration,newNumSamples, endpoint=False);
    return (time,data,downsampled_time, downsampled_signal,sampling_freq,downsampled_sampling_freq)
    
    

def plotAmplitudeSpectrum(signal,downsampledSignal,channelNumber,signalFreq,downsampledFreq):
    #signal = np.transpose(signal);
    #downsampledSignal = np.transpose(downsampledSignal);
    plt.magnitude_spectrum(signal[:,channelNumber],Fs=signalFreq)
    plt.savefig('figures/ampSpectrum.png')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Amplitude");
    plt.close()

    plt.magnitude_spectrum(downsampledSignal[:,channelNumber],Fs=downsampledFreq)
    plt.savefig('figures/ampSpectrumDownsampled.png')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Amplitude");
    plt.close()

    plt.magnitude_spectrum(signal[:,channelNumber],Fs=signalFreq,scale='dB')
    plt.savefig('figures/logAmpSpectrum.png')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Log(Amplitude)");
    plt.close()

    plt.magnitude_spectrum(downsampledSignal[:,channelNumber],Fs=downsampledFreq, scale='dB')
    plt.savefig('figures/logAmpSpectrumDownsampled.png')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Log(Amplitude)");
    plt.close()



def plotLowpass(time,signal,downsampleTime,downsampledSignal,channelNumber,startTime,endTime):
    temp = np.where(time >= startTime);
    first = min(min(temp));
    temp = np.where(time <= endTime);
    last = max(max(temp));
    
    temp = np.where(downsampleTime >= startTime);
    first_d = min(min(temp));
    temp = np.where(downsampleTime <= endTime);
    last_d = max(max(temp));
    
    
    fig = plt.figure(figsize=(10,10));
    plt.plot(time[first:last], signal[first:last,channelNumber], 'b-', label='signal')
    plt.plot(downsampleTime[first_d:last_d], downsampledSignal[first_d:last_d, channelNumber], 'r-', label='downsampled signal')
    plt.xlabel("Time (s)");
    plt.ylabel("Amplitude");
    plt.legend();
    plt.savefig('figures/lowpassFigure.png')
    plt.close()

    
def lowpass(data, freq, df, corners=4, zerophase=False):
    """
    Butterworth-Lowpass Filter.
​
    Filter data removing data over certain frequency ``freq`` using ``corners``
    corners.
    The filter uses :func:`scipy.signal.iirfilter` (for design)
    and :func:`scipy.signal.sosfilt` (for applying the filter).
​
    :type data: numpy.ndarray
    :param data: Data to filter.
    :param freq: Filter corner frequency.
    :param df: Sampling rate in Hz.
    :param corners: Filter corners / order.
    :param zerophase: If True, apply filter once forwards and once backwards.
        This results in twice the number of corners but zero phase shift in
        the resulting filtered trace.
    :return: Filtered data.
    """
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        f = 1.0
        msg = "Selected corner frequency is above Nyquist. " + \
              "Setting Nyquist as high corner."
        warnings.warn(msg)
    z, p, k = iirfilter(corners, f, btype='lowpass', ftype='butter',
                        output='zpk')
    sos = zpk2sos(z, p, k)
    if zerophase:
        firstpass = sosfilt(sos, data)
        return sosfilt(sos, firstpass[::-1])[::-1]
    else:
        return sosfilt(sos, data)


