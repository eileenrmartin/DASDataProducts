"""

"""


def t15_attempt():
    print("Fetch data from server attempt")
    
    #set up connection to server
    client = treble_setup.setup_server()

    #get few frames of reshaped data (2D, time samples by channels)
    output = treble_setup.get_data(client)
    
    #dt not even - fix everything
    #time window size must be either number of frames or number of time samples per frame
    
    #calculate number of frequencies to store
    num_freq = condenser.calc_num_freq(len(output), 89)
    
    #dT value from md, used to calculate nyquist
    nyq_freq = condenser.calc_nyq_freq(0.00044752)
    
    #get condensed matrix
    spect, std_devs, means, max_vals, peak_freq = condenser.condmatrix(output, 89, 4, 5, 50, 0, 248, num_freq, nyq_freq)
    
    print(spect.shape)
    
    #test plots
    
    clip = np.percentile(np.absolute(output),95)
    fig4 = plt.figure()
    img4 = plt.imshow(output, aspect='auto', interpolation='none', vmin=0, vmax=clip)#, extent=(-250, 250, num_time_windows, 0))
    plt.colorbar()
    plt.title('Server Data')
    plt.ylabel('Time sample')
    plt.xlabel('Channel')
    plt.savefig("./t15_figs/data.png")
    
    data_fft = np.abs(condenser.rfft(output))
    
    clip = np.percentile(np.absolute(data_fft),95)
    fig4 = plt.figure()
    img4 = plt.imshow(data_fft, aspect='auto', interpolation='none', vmin=0, vmax=clip)#, extent=(-250, 250, num_time_windows, 0))
    plt.colorbar()
    plt.title('Server Data - FFT')
    plt.ylabel('Freq (Hz)')
    plt.xlabel('Channel')
    plt.savefig("./t15_figs/fft.png")
    
    #plot one ch group
    cond_data = spect[:, 1, :]
    
    #plot one time window
    cond_win = spect[0, :, :]
    
    clip = np.percentile(np.absolute(cond_data),95)
    fig5 = plt.figure()
    img5 = plt.imshow(cond_data, aspect='auto')#, interpolation='none', vmin=0, vmax=clip)#, extent=(-250, 250, num_time_windows, 0))
    plt.colorbar()
    plt.title('Server Data - Channel Group: 1')
    plt.ylabel('Time window (len of 4 samples)')
    plt.xlabel('Frequency (Hz)')
    plt.savefig("./t15_figs/ch_group.png")
    
    clip = np.percentile(np.absolute(cond_win),95)
    fig6 = plt.figure()
    img6 = plt.imshow(cond_win, aspect='auto')#, interpolation='none', vmin=0, vmax=clip)#, extent=(-250, 250, num_sensor_groups, 0))
    plt.colorbar()
    plt.title('Server Data - Time Window: 0')
    plt.ylabel('Channel (group of 100)')
    plt.xlabel('Frequency (Hz)')
    plt.savefig("./t15_figs/tw.png")