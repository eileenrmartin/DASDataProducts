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
	#Run lowpass filter and downsample 
	(time, signal, downsample_time, downsample_signal, sample_freq, downsampled_sample_freq) = lowpassDownsample.runLowpassAndDownsampleWithFile(integerDownsampleFactor,fileName);
	print(downsample_signal.shape, file=sys.stderr);
	#img = plt.imshow(downsample_signal, aspect='auto',interpolation='none');
	#plt.ylabel('Amp')
	#plt.xlabel('Time')
	#img = ds.tf.shade(signal, cmap=fire, how='linear')
#export_image(img, "out", background="black", export_path="figures/")
	plt.imshow(signal,aspect='auto',interpolation='nearest',vmin=-1*np.percentile(signal,99),vmax=np.percentile(signal,99),cmap='seismic');
	plt.colorbar()
	plt.savefig('figures/rasterPlot.png');
if __name__ == "__main__":
	main(sys.argv[1:])

