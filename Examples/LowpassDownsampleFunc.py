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

def fetchT15LocalServerData():
    client = server_func.setup_server();
    data, md = server_func.get_data(client,1);
    dT = md['dT'];
    sampling_freq = 1/dT;
    number_time_samples = md['nT'];
    sampling_duration = number_time_samples * dT;
    return (np.transpose(data), sampling_duration, number_time_samples,sampling_freq)  

def getFileData(fileName):
    f = h5py.File(fileName, 'r');
    group = f['data_product'];
    data = group['data'][()];
    dT = f.attrs['dt_computer'];
    sampling_freq = 1/dT;
    number_time_samples = f.attrs['nt'];
    sampling_duration = number_time_samples * dT;
    return (data, sampling_duration, number_time_samples,sampling_freq)  

def runLpAndDs(data, dT, sampling_freq, number_of_time_samples, integerDownsampleFactor):
    data_T = np.transpose(data);
    sampling_duration = number_of_time_samples * dT;
    time = np.linspace(0, sampling_duration, number_of_time_samples, endpoint=False);
    downsampled_signal = scipy.signal.decimate(data,integerDownsampleFactor,ftype="iir");
    newNumSamples = len(downsampled_signal[0]);
    downsampled_time = np.linspace(0,sampling_duration,newNumSamples, endpoint=False);
    return (time,data_T,downsampled_time, downsampled_signal,sampling_freq)

def runLowpassAndDownsample(data, sampling_duration, number_time_samples, sampling_freq, integerDownsampleFactor):
    downsampled_sampling_freq = sampling_freq/integerDownsampleFactor
    time = np.linspace(0, sampling_duration, number_time_samples, endpoint=False);
    data_T = np.transpose(data);
    #print(data_T.shape, file = sys.stderr);
    #n = len(data_T[0])
    #window = scipy.signal.cosine(n)
    #data_T *= window
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
    plt.magnitude_spectrum(downsampledSignal[channelNumber,:],Fs=downsampledFreq)
    plt.savefig('figures/ampSpectrumDownsampled.png')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Amplitude");
    plt.close()

    plt.magnitude_spectrum(signal[:,channelNumber],Fs=signalFreq,scale='dB')
    plt.savefig('figures/logAmpSpectrum.png')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Log(Amplitude)");
    plt.close()

    plt.magnitude_spectrum(downsampledSignal[channelNumber,:],Fs=downsampledFreq, scale='dB')
    plt.savefig('figures/logAmpSpectrumDownsampled.png')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Log(Amplitude)");
    plt.close()


def plotLowpass(time,signal,channelNumber):
    
    
    fig = plt.figure(figsize=(10,10));
    plt.plot(time, np.transpose(signal[:,channelNumber]), 'b-', label='signal')
    
    #plt.plot(time, signal[:,channelNumber], 'b-', label='signal')
    #plt.plot(downsampleTime, downsampledSignal[:, channelNumber], 'r-', label='downsampled signal')
    plt.xlabel("Time (s)");
    plt.ylabel("Amplitude");
    plt.legend();
    plt.savefig('figures/lowpassFigure.png')
    plt.close()


def plotDownsample(downsampleTime,downsampleSignal,channelNumber):
    
    
    fig = plt.figure(figsize=(10,10));
    plt.plot(downsampleTime, downsampleSignal[channelNumber,:], 'b-', label='signal')
    
    #plt.plot(time, signal[:,channelNumber], 'b-', label='signal')
    #plt.plot(downsampleTime, downsampledSignal[:, channelNumber], 'r-', label='downsampled signal')
    plt.xlabel("Time (s)");
    plt.ylabel("Amplitude");
    plt.legend();
    plt.savefig('figures/downsampleFigure.png')
    plt.close()

def plotLowpassDownsample(time,signal,downsampleTime,downsampledSignal,channelNumber,startTime,endTime):
    temp = np.where(time >= startTime);
    first = min(min(temp));
    temp = np.where(time <= endTime);
    last = max(max(temp));
    
    temp = np.where(downsampleTime >= startTime);
    first_d = min(min(temp));
    temp = np.where(downsampleTime <= endTime);
    last_d = max(max(temp));
    
    
    fig = plt.figure(figsize=(10,10));
    plt.plot(time, signal[:,channelNumber], 'b-', label='signal')
    plt.plot(downsampleTime, downsampledSignal[channelNumber,:], 'r-', label='downsampled signal')
    
    #plt.plot(time, signal[:,channelNumber], 'b-', label='signal')
    #plt.plot(downsampleTime, downsampledSignal[:, channelNumber], 'r-', label='downsampled signal')
    plt.xlabel("Time (s)");
    plt.ylabel("Amplitude");
    plt.legend();
    plt.savefig('figures/lowpassAndDownsampleFigure.png')
    plt.close()
