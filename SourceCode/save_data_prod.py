#!/usr/bin/env python3

""" Save Data Products From Stream

This script is meant to be called repeatedly to continuously fetch data from a treble server 
and calculate and store data products in a file. 

Author(s)
---------
Samantha Paulus
"""

from T15 import server_func
import sys
import lowpassDownsample

if __name__ == '__main__':
    print("Fetch data from server attempt")
    
    #get name of param file to use
    filename = sys.argv[1]
    
    server_func.save_file(filename)
