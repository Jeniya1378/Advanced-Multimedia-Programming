'''
CSC 745 Advanced Multimedia Programming
Calculate and plot zero crossings of an input sound
Jeniya Sultana
'''
from scipy.io import wavfile
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

MAX_INT16 = 32767
INT16_DTYPE = "int16"

fname_speech = "birch_canoe.wav"

def read_wave(fname):
    '''Reads a wave file and returns the sample rate and samples'''
    rate, data = wavfile.read(fname)
    return rate, data

def plot_wave2(sig1, sig2, title0, title1):
    '''Plots two signals'''
    fig, ax = plt.subplots(nrows = 2, figsize = (12, 4))
    ax[0].plot(np.arange(len(sig1)), sig1, linestyle = '-')
    ax[1].plot(np.arange(len(sig2)), sig2, linestyle = '-')
    ax[0].set_title(title0)
    ax[1].set_title(title1)
    plt.subplots_adjust(hspace=0.5)
    plt.show()

def calc_zc(sig, fs):
    '''Calculates zero crossings and returns it'''
    win_len = int(fs/50)  #20 ms window

    # Initializing array to store the zero-crossings envelope
    zero_crossings_envelope = np.zeros(len(sig))

    # Iterating through the audio signal in steps 
    for i in range(0, len(sig), win_len):
        window_start = i
        window_end = min(i + win_len, len(sig))
        
        # Calculating zero-crossings in each current analysis window
        zero_crossings = 0
        for j in range(window_start + 1, window_end):
            if (sig[j-1] >= 0 and sig[j] < 0) or (sig[j-1] < 0 and sig[j] >= 0):
                zero_crossings += 1
        
        # Storing value
        zero_crossings_envelope[window_start:window_end] = zero_crossings
    
    return zero_crossings_envelope

def difference(sig):
    '''Differences a sound and returns the differenced samples'''
    ...  #Your code here to difference the signal and return it
     # Compute the discrete derivative
    diff_signal = np.diff(sig) 
    # Since diff() reduces the size of the array by 1, hence adding a 0 at the beginning to match sizes
    diff_signal = np.insert(diff_signal, 0, 0)
    return diff_signal

def scale_signal(signal, target_value, data_type):
    scale_factor = target_value/np.abs(signal).max()
    new_signal = np.array(signal*scale_factor, dtype = data_type)
    return new_signal

def main():
    fs, snd = read_wave(fname_speech)
    diff_sig = difference(snd[16000:40000])
    sd.play(snd[16000:40000], fs)
    sd.wait()
    sd.play(diff_sig, fs)
    sd.wait()
    scaled_wave = scale_signal(diff_sig, MAX_INT16, INT16_DTYPE)
    sd.play(scaled_wave, fs)
    sd.wait()
    zero_crossings_original_signal = calc_zc(snd[16000:40000], fs)  
    zero_crossings_diff_signal = calc_zc(diff_sig, fs)
    plot_wave2(snd[16000:40000], zero_crossings_original_signal, "Audio Signal", "Zero Crossings")
    plot_wave2(diff_sig, zero_crossings_diff_signal, "Differentiated Signal", "Zero Crossings")


main()
