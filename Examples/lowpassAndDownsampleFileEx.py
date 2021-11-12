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
	integerDownsampleFactor = 10;
	#Get data
	(data, sampling_duration, number_time_samples, sampling_freq) = lowpassDownsample.getFileData(fileName);
	#Run lowpass filter and downsample 
	(time, signal, downsample_time, downsample_signal, sample_freq, downsampled_sample_freq) = lowpassDownsample.runLowpassAndDownsample(data,sampling_duration,number_time_samples,sampling_freq,integerDownsampleFactor);
	channelNumber = 30;
	#print(downsample_time.shape, file = sys.stderr);
	print(downsample_signal[channelNumber,:].shape, file = sys.stderr);
	#Plot lowpass filter on channelNumber
	lowpassDownsample.plotLowpassDownsample(time,signal,downsample_time,downsample_signal,channelNumber);
	
	#lowpassDownsample.plotLowpass(time,signal,channelNumber);
	lowpassDownsample.plotAmplitudeSpectrum(signal, downsample_signal, channelNumber, sample_freq,downsampled_sample_freq);
	#lowpassDownsample.plotDownsample(downsample_time,downsample_signal,channelNumber);
if __name__ == "__main__":
	main(sys.argv[1:])

