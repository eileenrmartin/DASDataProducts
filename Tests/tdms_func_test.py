import unittest
import sys
sys.path.insert(1, '../SourceCode')
from Silixa import tdms_func
import numpy as np
from datetime import datetime, timedelta
import pytz

class TestCond(unittest.TestCase):
    
    def test_ch_ind_array(self):
        
        ch_ind = tdms_func.ch_ind_array(25)
        
        #first index should be the number of groups
        self.assertEqual(ch_ind[0], 25, "Should be 25 channel groups")
        
        #ch group size from params file
        g_size = 100
        #last channel index from params file
        last_channel = 2431
        
        #next values should be starting and ending indexes of first channel group, second, third, etc
        for i in range(25):
            self.assertEqual(ch_ind[2*i + 1], i * g_size, "Checking start index of channel group")
            if i == 24:
                self.assertEqual(ch_ind[2*i + 2], last_channel, "Checking end index of channel group")
            else:
                self.assertEqual(ch_ind[2*i + 2], (i * g_size) + (g_size - 1), "Checking end index of channel group")
    
    def test_tw_ind_array(self):
        tw_ind = tdms_func.tw_ind_array(500, 5, 10)
        
        #first index is length of window in seconds
        self.assertEqual(tw_ind[0], 2, "Should be two seconds")
        
        #next index is number of time windows
        self.assertEqual(tw_ind[1], 10, "Should be 10")
        
        #next are datetimes of starting time at each time window
        
        #starting time
        start_dttime = datetime(2019, 4, 26, 20, 54, 0, 0, tzinfo=pytz.UTC)
        
        for j in range(30 * 5):
            self.assertTrue(tw_ind[j + 2] == start_dttime + timedelta(seconds=(j * 2)), "Check datetime of start of timewindow")
    
    def test_freq_ind_array(self): 
        freq_ind = tdms_func.freq_ind_array(250, 167)
        
        #first value is number of freq bins
        self.assertEqual(freq_ind[0], 167, "Should be 167 freq bins")
        #next value is width of each bin in hz
        self.assertEqual(freq_ind[1], (250/167), "Should be about 1.497 Hz")
        #last value is nyquist freq
        self.assertEqual(freq_ind[2], 250, "Should be 250 Hz")

if __name__ == '__main__':
    unittest.main()