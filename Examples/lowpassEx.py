import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys
sys.path.insert(1, '../SourceCode')
import lowpass
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
plt.switch_backend('agg')

filterOrder = 6;
integerDownsampleFactor = 10;
#Run lowpass filter
(time,signal,filtered_signal,num_samples,sample_duration,sample_freq) = lowpass.runLowpass(integerDownsampleFactor,filterOrder);
(downsample_time, downsample_signal) = lowpass.runDownsample(integerDownsampleFactor,sample_duration,filtered_signal);
channelNumber = 50;
startTime = 0.10;
endTime = 0.15;

#Plot lowpass filter on channelNumber
lowpass.plotLowpass(time,signal,filtered_signal,downsample_time,downsample_signal,channelNumber,startTime,endTime);
lowpass.plotAmplitudeSpectrum(signal, filtered_signal, channelNumber, num_samples, sample_freq);

