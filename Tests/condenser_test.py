import unittest
import sys
sys.path.insert(1, '../SourceCode')
import condenser
import numpy as np

class TestCond(unittest.TestCase):

    def test_calc_num_ch_groups(self):
        self.assertEqual(condenser.calc_num_ch_groups(1, 10, 1), 10, "Should be 10 channel groups")
        self.assertEqual(condenser.calc_num_ch_groups(0, 2431, 100), 25, "Should be 25 channel groups")

    def test_calc_num_time_win(self):
        self.assertEqual(condenser.calc_num_time_win(1, 10, 1), 10, "Should be 10 time windows")
        self.assertEqual(condenser.calc_num_time_win(0, 29999, 1000), 30, "Should be 30 time windows")
    
    def test_calc_num_freq(self):
        self.assertEqual(condenser.calc_num_freq(10, 1), 6, "Should be 6 frequencies")
        self.assertEqual(condenser.calc_num_freq(30000, 30), 501, "Should be 501 frequencies")
    
    def test_time_stats(self):
        #create 2D array of alternating 1's and -1's
        data = np.ones((6,4), np.int32)
        data[::2,::2] = -1
        data[1::2,1::2] = -1
        
        #test mean
        ch_means = condenser.mean_time(data)
        self.assertEqual(ch_means[0], 0, "Mean should be 0")
        self.assertEqual(ch_means[1], 0, "Mean should be 0")
        self.assertEqual(ch_means[2], 0, "Mean should be 0")
        self.assertEqual(ch_means[3], 0, "Mean should be 0")
        
        #test std dev
        std_devs = condenser.std_dev_time(data)
        self.assertEqual(std_devs[0], 1, "Std dev should be 0")
        self.assertEqual(std_devs[1], 1, "Std dev should be 0")
        self.assertEqual(std_devs[2], 1, "Std dev should be 0")
        self.assertEqual(std_devs[3], 1, "Std dev should be 0")
        
        #add max values to data
        data[0, 0] = 2
        data[1, 1] = 3
        data[2, 2] = 4
        data[3, 3] = 5
        
        #test max values
        ch_maxs = condenser.max_time(data)
        self.assertEqual(ch_maxs[0], 2, "Max should be 2")
        self.assertEqual(ch_maxs[1], 3, "Max should be 3")
        self.assertEqual(ch_maxs[2], 4, "Max should be 4")
        self.assertEqual(ch_maxs[3], 5, "Max should be 5")    
    
    def test_condmatrix(self):
        #calculate fft for test
        #create 2D array of alternating 1's and -1's
        data = np.ones((10,8), np.int32)
        data[::2,::2] = -1
        data[1::2,1::2] = -1
        
        data_fft = np.abs(condenser.rfft(data))
        #print(condenser.rfft(data))
        #print(data_fft)
        
        n_freq = condenser.calc_num_freq(len(data), 5)
        
        spect, std_devs, means, max_vals, peak_freq = condenser.condmatrix(data, 5, 2, 4, 2, 0, 7, n_freq, 10)
        
        test_spect = np.zeros((5, 4, 2))
        test_spect[:, :, 1] = 2
        
        #check spect is calculating correctly
        self.assertTrue(np.array_equal(spect, test_spect), "Arrays should be equal")
        
        #check std_deviations
        test_std = np.ones((5, 4))
        
        self.assertTrue(np.array_equal(std_devs, test_std), "Std deviations should be 1")
        
        #check mean values
        test_means = np.ones(8)
        
        self.assertTrue(np.array_equal(means, test_means), "Means should be 1")
        
        #check maximum values
        test_maxs = np.full(8, 2)
        
        self.assertTrue(np.array_equal(max_vals, test_maxs), "Maximum values should be 2")
        
        #check peak_frequency
        self.assertEqual(peak_freq, 5.0, "Peak freq should be 5.0")
        

if __name__ == '__main__':
    unittest.main()