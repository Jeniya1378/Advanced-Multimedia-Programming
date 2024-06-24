'''
CSC 745 Advanced Multimedia Programming
Calculate and plot RMS of an input sound
Name: Jeniya Sultana
'''
from scipy.io import wavfile
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

fname_speech = "Asn_RMS//birch_canoe.wav"

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
    fig.tight_layout()
    plt.show()

def calc_rms(sig, fs):
    '''Calculates the rms of a signal; use 25 ms window length.
       Returns an array of RMS values.'''
    ...  #Your code here
    window_length = 25
    # Converting from ms to seconds
    window_length_in_seconds = window_length/1000
    window_length_samples = int(window_length_in_seconds * fs) 
    rms_values = []

    for i in range(0, len(sig), window_length_samples):
        window = sig[i:i + window_length_samples]
        rms = np.sqrt(np.mean(np.square(window)))
        rms_values.append(rms)

    return rms_values

def main():
    fs, snd = read_wave(fname_speech)
    rms = calc_rms(snd[16000:40000], fs)
    # sd.play(snd[16000:40000], fs)
    plot_wave2(snd[16000:40000], rms, "Audio Signal", "RMS Energy")
    # sd.wait()

main()
