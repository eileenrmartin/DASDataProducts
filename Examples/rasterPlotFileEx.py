import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys
sys.path.insert(1, '../SourceCode')
import lowpassDownsample
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
import time
import seaborn as sns
from datashader import transfer_functions as tf, reductions as rd

plt.switch_backend('agg')


def main(argv):
	fileName = argv[0]
	integerDownsampleFactor = 10;
	#Run lowpass filter and downsample 
	(time, signal, downsample_time, downsample_signal, sample_freq, downsampled_sample_freq) = lowpassDownsample.runLowpassAndDownsampleWithFile(integerDownsampleFactor,fileName);
	print(downsample_signal.shape, file=sys.stderr);
	#img = plt.imshow(downsample_signal, aspect='auto',interpolation='none');
	#plt.ylabel('Amp')
	#plt.xlabel('Time')
	img = ds.tf.shade(signal, cmap=fire, how='linear')
export_image(img, "out", background="black", export_path="figures/")

if __name__ == "__main__":
	main(sys.argv[1:])

