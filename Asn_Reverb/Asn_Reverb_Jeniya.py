'''
CSC 745 Advanced Multimedia Programming
Assignment: Add reverb or echo to a recorded sound
Name: Jeniya Sultana

Crossfade one sound into another
'''
from scipy.io import wavfile
import numpy as np
import sounddevice as sd

filename = "birch_canoe.wav"

def read_wave(fname):
    '''Reads a wave file and returns sample rate and samples'''
    rate, data = wavfile.read(fname)
    return rate, data

def reverb(snd, delay, rev_amp, rate):
    '''Returns a reverberated copy of snd; delay is in ms
       rev_amp is multiplier for delayed samples'''
    #Hint: sample rate / 1000 gives the number of samples in 1 ms
    # Convert delay from milliseconds to the number of samples
    delay_samples = int(delay * rate / 1000)
    reverb_snd = np.copy(snd)
    copy_original_snd = np.copy(snd)

    for i in range(len(snd)):
        if i >= delay_samples:
            reverb_snd[i] = (1-rev_amp) * copy_original_snd[i] + rev_amp * reverb_snd[i - delay_samples]

    return reverb_snd #Change this to return your modified sound

def main():
    delay = 500     #Delay in ms
    delay_amp = .3  #Multiplier for delayed samples
    rate, snd = read_wave(filename)
    new_snd = reverb(snd, delay, delay_amp, rate)
    sd.play(new_snd, rate)  #Play the reverberated sound
    sd.wait()  #Wait until the sound is finished playing

main()

    
