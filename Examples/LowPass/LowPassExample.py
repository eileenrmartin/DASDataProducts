import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
plt.switch_backend('agg')

order = 5

sampling_freq = 30

cutoff_freq = 2

sampling_duration = 5

number_of_samples = sampling_freq * sampling_duration

time = np.linspace(0, sampling_duration, number_of_samples, endpoint=False)

signal = np.sin(2*np.pi*10*time) + np.sin(2*np.pi*2*time)

normalized_cutoff_freq = 2 * cutoff_freq / sampling_freq

numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff_freq)

filtered_signal = scipy.signal.lfilter(numerator_coeffs, denominator_coeffs, signal)

plt.plot(time, signal, 'b-', label='signal')
plt.plot(time, filtered_signal, 'g-', linewidth=2, label='filtered signal')
plt.legend()
plt.savefig('../figures/lowPass.png')
plt.clf()
