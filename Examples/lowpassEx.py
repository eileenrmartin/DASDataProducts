import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys
sys.path.insert(1, '../SourceCode')
import lowpass
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
plt.switch_backend('agg')

cutoffFrequency = 80;
filterOrder = 4;
#Run lowpass filter
(time,signal,filtered_signal, num_samples, sample_freq) = lowpass.runLowpass(cutoffFrequency,filterOrder);

channelNumber = 50;
startTime = 0.10;
endTime = 0.15;

#Plot lowpass filter on channelNumber
(signal_on_channel, filtered_signal_on_channel) = lowpass.plotLowpass(time,signal,filtered_signal,channelNumber,startTime,endTime);
#lowpass.testFunc1(signal_on_channel, num_samples, sample_freq);
#(signal_rfft, filtered_signal_rfft) = lowpass.testFunc(signal_on_channel,filtered_signal_on_channel);
#lowpass.plotAmplitudeSpectrum(time,signal_rfft, filtered_signal_rfft,preAmp, postAmp, channelNumber, startTime, endTime);

