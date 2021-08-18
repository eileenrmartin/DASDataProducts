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

(time,signal,filtered_signal) = lowpass.runLowpass(cutoffFrequency,filterOrder);

channelNumber = 50;
startTime = 0.10;
endTime = 0.15;
lowpass.plotLowpass(time,signal,filtered_signal,channelNumber,startTime,endTime);
#(preAmp, postAmp) = lowpass.testFunc(signal,filtered_signal);
#lowpass.plotAmplitudeSpectrum(time,preAmp, postAmp);

