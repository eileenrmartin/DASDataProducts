import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from T15 import server_func
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
import sys

def main():
    plt.switch_backend('agg')
    client = server_func.setup_server();
    data, md = server_func.get_data(client,1);
    cutoff_freq = 2;
    sampling_rate = md['dx'];
    #print(sampling_rate, file = sys.stdout);
    lowpassData = lowpass(data, cutoff_freq, sampling_rate, 6, zerophase=True);
    print(md, file = sys.stdout);

def plotLowpass(numSamples,time,signal,filteredSignal):
    number_of_samples = server_func.calc
    time = np.linspace(0, sampling_duration, number_of_samples, endpoint=False)
    plt.plot(time, signal, 'b-', label='signal')
    plt.plot(time, filtered_signal, 'g-', linewidth=2, label='filtered signal')
    plt.legend()
    plt.savefig('../figures/lowPass.png')
    plt.clf()

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

if __name__ == '__main__':
    main()
