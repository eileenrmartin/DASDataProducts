import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys
sys.path.insert(1, '../SourceCode')
import lowpass
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
plt.switch_backend('agg')

(time,signal,filtered_signal) = lowpass.runLowpass(50,6);
lowpass.plotLowpass(time,signal,filtered_signal);


