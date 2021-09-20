import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys
sys.path.insert(1, '../SourceCode')
import lowpass
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
plt.switch_backend('agg')

integerDownsampleFactor = 8;
#Run lowpass filter
#(time,signal,filtered_signal,num_samples,sample_duration,sample_freq) = lowpass.runLowpass(integerDownsampleFactor,filterOrder);
(time, signal, downsample_time, downsample_signal, sample_freq) = lowpass.runDownsample(integerDownsampleFactor);
#(time,signal,filtered_signal,num_samples,sample_duration,sample_freq) = lowpass.runLowpass(integerDownsampleFactor,filterOrder);

channelNumber = 50;
startTime = 0.05;
endTime = 0.15;

#Plot lowpass filter on channelNumber
lowpass.plotLowpass(time,signal,downsample_time,downsample_signal,channelNumber,startTime,endTime);
lowpass.plotAmplitudeSpectrum(signal, downsample_signal, channelNumber, sample_freq);

