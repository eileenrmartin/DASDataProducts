""" Save Data Products From Stream

This script is meant to be called repeatedly to continuously fetch data from a treble server 
and calculate and store data products in a file. 

"""

from T15 import server_func
import sys

    
    #dt not even - fix everything - changes sampling freq, nyq freq
    #time window size must be either number of frames or number of time samples per frame
    
    


if __name__ == '__main__':
    print("Fetch data from server attempt")
    
    
    #get name of param file to use
    filename = sys.argv[1]
    
    server_func.save_file(filename)