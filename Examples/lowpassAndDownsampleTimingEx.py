import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import sys
sys.path.insert(1, '../SourceCode')
import lowpass
from scipy.signal import iirfilter, zpk2sos, sosfilt
import warnings
import time
plt.switch_backend('agg')


#Time lowpass filter and downsample 
var = sys.stdout;
integerDownsampleFactor = 2;
runs = 4;
t1 = time.process_time();
for i in range(runs):
    (tm, signal, downsample_time, downsample_signal, sample_freq) = lowpass.runLowpassAndDownsample(integerDownsampleFactor);
t2 = time.process_time();
var.write("Average time of runLowpassAndDownsample(integerDownsampleFactor) with integer downsample factor of " + str(integerDownsampleFactor) + " and number of runs equal to " + str(runs) + "\n");
avg = (t2-t1)/runs;
var.write(str(avg) + " seconds \n");

var = sys.stdout;
integerDownsampleFactor = 4;
runs = 4;
t1 = time.process_time();
for i in range(runs):
    (tm, signal, downsample_time, downsample_signal, sample_freq) = lowpass.runLowpassAndDownsample(integerDownsampleFactor);
t2 = time.process_time();
var.write("Average time of runLowpassAndDownsample(integerDownsampleFactor) with integer downsample factor of " + str(integerDownsampleFactor) + " and number of runs equal to " + str(runs) + "\n");
avg = (t2-t1)/runs;
var.write(str(avg) + " seconds \n");

var = sys.stdout;
integerDownsampleFactor = 6;
runs = 4;
t1 = time.process_time();
for i in range(runs):
    (tm, signal, downsample_time, downsample_signal, sample_freq) = lowpass.runLowpassAndDownsample(integerDownsampleFactor);
t2 = time.process_time();
var.write("Average time of runLowpassAndDownsample(integerDownsampleFactor) with integer downsample factor of " + str(integerDownsampleFactor) + " and number of runs equal to " + str(runs) + "\n");
avg = (t2-t1)/runs;
var.write(str(avg) + " seconds \n");

var = sys.stdout;
integerDownsampleFactor = 8;
runs = 4;
t1 = time.process_time();
for i in range(runs):
    (tm, signal, downsample_time, downsample_signal, sample_freq) = lowpass.runLowpassAndDownsample(integerDownsampleFactor);
t2 = time.process_time();
var.write("Average time of runLowpassAndDownsample(integerDownsampleFactor) with integer downsample factor of " + str(integerDownsampleFactor) + " and number of runs equal to " + str(runs) + "\n");
avg = (t2-t1)/runs;
var.write(str(avg) + " seconds \n");


