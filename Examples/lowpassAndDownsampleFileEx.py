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


def main(argv):
	fileName = argv[0]
	integerDownsampleFactor = 8;
	#Run lowpass filter and downsample 

	(time, signal, downsample_time, downsample_signal, sample_freq, downsampled_sample_freq) = lowpassDownsample.runLowpassAndDownsampleWithFile(integerDownsampleFactor,fileName);
	channelNumber = 60;
	startTime = 3.00;
	endTime = 11.0;

	#Plot lowpass filter on channelNumber
	lowpassDownsample.plotLowpass(time,signal,downsample_time,downsample_signal,channelNumber,startTime,endTime);
	lowpassDownsample.plotAmplitudeSpectrum(signal, downsample_signal, channelNumber, sample_freq,downsampled_sample_freq);
if __name__ == "__main__":
	main(sys.argv[1:])

