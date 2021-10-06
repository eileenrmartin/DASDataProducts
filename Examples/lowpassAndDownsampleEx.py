import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys
sys.path.insert(1, '../SourceCode')
import lowpassDownsample
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
import time
plt.switch_backend('agg')

integerDownsampleFactor = 8;
#Run lowpass filter and downsample 

(time, signal, downsample_time, downsample_signal, sample_freq) = lowpassDownsample.runLowpassAndDownsample(integerDownsampleFactor);

channelNumber = 50;
startTime = 0.05;
endTime = 0.15;

#Plot lowpass filter on channelNumber
lowpassDownsample.plotLowpass(time,signal,downsample_time,downsample_signal,channelNumber,startTime,endTime);
lowpassDownsample.plotAmplitudeSpectrum(signal, downsample_signal, channelNumber, sample_freq);

