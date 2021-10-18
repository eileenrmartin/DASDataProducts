#!/usr/bin/env python3

""" Save Data Products From Stream

This script is meant to be called repeatedly to continuously fetch data from a treble server 
and calculate and store data products in a file. 

"""

from T15 import server_func
import sys
import lowpassDownsample

if __name__ == '__main__':
    print("Fetch data from server attempt")
    
    #get name of param file to use
    filename = sys.argv[1]
    
    server_func.save_file(filename)
    #(time,signal,downsample_time, downsample_signal,sample_freq) = lowpassDownsample.runLowpassAndDownsample(2)
    
    #channelNumber = 50;
    #startTime = 0;
    #endTime = 0.15;
    #print(signal.shape)
    #print(time.shape)
    #import numpy as np 
    #signal = np.transpose(signal)
    #print(downsample_signal.shape)
    #print(downsample_time.shape)
    #downsample_signal = np.transpose(downsample_signal)
    #Plot lowpass filter on channelNumber
    #lowpassDownsample.plotLowpass(time,signal,downsample_time,downsample_signal,channelNumber,startTime,endTime);
    #lowpassDownsample.plotAmplitudeSpectrum(signal, downsample_signal, channelNumber, sample_freq, sample_freq);