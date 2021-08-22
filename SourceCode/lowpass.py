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

def plotAmplitudeSpectrum(signal,filteredSignal,channelNumber,numSamples, signalFreq):
    signal = np.transpose(signal);
    filteredSignal = np.transpose(filteredSignal);
    #print(signal.shape, file=sys.stderr)
    normalized_signal = np.int16((signal / signal.max()) * 32767)
    normalized_filtered_signal = np.int16((filteredSignal / filteredSignal.max()) * 32767)
    #print(normalized_tone.shape, file=sys.stderr)
    yf1 = rfft(normalized_signal[:,channelNumber]);
    xf = rfftfreq(numSamples, signalFreq);
    yf2 = rfft(normalized_filtered_signal[:,channelNumber]);

    plt.plot(xf, np.abs(yf1), 'b-', label='amplitude spectrum of signal')
    plt.legend();
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Amplitude");
    plt.savefig('figures/amplitudeSpectrum.png')
    plt.close()

    plt.plot(xf, np.abs(yf2), 'r-', label='amplitude spectrum of filtered signal')
    plt.legend();
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Amplitude");
    plt.savefig('figures/amplitudeSpectrumOfFilteredSignal.png')
    plt.close()
    
    plt.plot(xf, np.abs(yf1), 'b-', label='amplitude spectrum of signal')
    plt.yscale("log");
    plt.legend();
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Log(Amplitude)");
    plt.savefig('figures/logAmplitudeSpectrum.png')
    plt.close()

    plt.plot(xf, np.abs(yf2), 'r-', label='amplitude spectrum of filtered signal')
    plt.yscale("log");
    plt.legend();
    plt.xlabel("Frequency (Hz)");
    plt.ylabel("Log(Amplitude)");
    plt.savefig('figures/logAmplitudeSpectrumOfFilteredSignal.png')
    plt.close()

    plt.magnitude_spectrum(signal[:,channelNumber],Fs=1/signalFreq)
    plt.savefig('figures/test.png')
    plt.close()

    plt.magnitude_spectrum(filteredSignal[:,channelNumber],Fs=1/signalFreq)
    plt.savefig('figures/test1.png')
    plt.close()



def plotLowpass(time,signal,filteredSignal,channelNumber,startTime,endTime):
    temp = np.where(time >= startTime);
    first = min(min(temp));
    temp = np.where(time <= endTime);
    last = max(max(temp));
    fig = plt.figure(figsize=(10,10));
    plt.plot(time[first:last], signal[first:last,channelNumber], 'b-', label='signal')
    plt.plot(time[first:last], filteredSignal[first:last, channelNumber], 'g-', label='filtered signal')
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


