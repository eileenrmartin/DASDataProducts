import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from T15 import server_func
import condenser
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
from scipy.fft import rfft, rfftfreq
import sys
plt.switch_backend('agg')

def runLowpass(cutoffFrequency, filterOrder):
    
    client = server_func.setup_server();
    data, md = server_func.get_data(client,1);
    cutoff_freq = cutoffFrequency;
    dT = md['dT'];
    sampling_freq = 1/dT;
    data_T = np.transpose(data);
    lowpassData = lowpass(data_T, cutoff_freq, sampling_freq, filterOrder, zerophase=True);
    number_of_time_samples = md['nT'];
    sampling_duration = number_of_time_samples * dT;
    time = np.linspace(0, sampling_duration, number_of_time_samples, endpoint=False)
    
    return (time, data_T, lowpassData, number_of_time_samples, sampling_freq)

def testFunc1(signal,numSamples, signalFreq):
    yf = rfft(signal);
    xf = rfftfreq(numSamples, signalFreq);
    print(signal.shape, file=sys.stderr);
    print(yf.shape, file=sys.stderr);
    print(numSamples, file=sys.stderr);
    print(signalFreq, file=sys.stderr);
    plt.plot(xf, np.abs(yf))
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Amplitude");
    plt.savefig('figures/amplitudeSpectrum.png')
    plt.close()

def testFunc(signal,filteredSignal):
    #signal_T = np.transpose(signal);
    #filteredSignal_T = np.transpose(filteredSignal);
    print(signal.shape, file=sys.stderr);
    print(filteredSignal.shape, file=sys.stderr);
    rfftPre = np.fft.rfft(signal);
    rfftPost = np.fft.rfft(filteredSignal);
    print(np.abs(rfftPre).shape, file=sys.stderr);
    
    return (np.abs(rfftPre), np.abs(rfftPost))

def plotAmplitudeSpectrum(time,signalOnChannel,filteredSignalOnChannel, rfftSignal, rfftFilteredSignal, channelNumber, startTime, endTime):
    #print(signalOnChannel, file=sys.stderr);
    #print(filteredSignalOnChannel.shape, file=sys.stderr);
    
    
    print(signalOnChannel.shape, file=sys.stderr);
    print(rfftSignal.shape, file=sys.stderr);
    plt.plot(signalOnChannel, rfftSignal, 'b-', label='amplitude spectrum of signal')
    #plt.plot(time, np.transpose(rfftFilteredSignal), 'g-', label='amplituded spectrum of filtered signal')
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Amplitude");
    plt.savefig('figures/amplitudeSpectrum.png')
    plt.close()

def plotLowpass(time,signal,filteredSignal,channelNumber,startTime,endTime):
    temp = np.where(time >= startTime);
    first = min(min(temp));
    temp = np.where(time <= endTime);
    last = max(max(temp));
    fig = plt.figure(figsize=(10,10))
    #print(signal.shape, file=sys.stderr);
    #print(filteredSignal.shape, file=sys.stderr);
    #print(signal[first:last,channelNumber], file=sys.stderr);
    #print(filteredSignal[first:last, channelNumber], file=sys.stderr);
    plt.plot(time[first:last], signal[first:last,channelNumber], 'b-', label='signal')
    plt.plot(time[first:last], filteredSignal[first:last, channelNumber], 'g-', label='filtered signal')
    plt.xlabel("Time (s)");
    plt.ylabel("Frequency (Hz)");
    plt.legend();
    plt.savefig('figures/lowpassFigure.png')
    plt.close()
    return (signal[first:last,channelNumber], filteredSignal[first:last, channelNumber])

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


