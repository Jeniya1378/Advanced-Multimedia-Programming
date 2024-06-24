'''
Create Spectrograms: Wideband and Narrowband
Adds sounddevice to play wav files
Updated to use scipy.fft
from: https://courses.engr.illinois.edu/ece590sip/sp2018/spectrograms1_wideband_narrowband.html
'''
import soundfile as sf #Reading
import sounddevice as sd #Playing
import numpy as np #Storing data
import scipy
import matplotlib.pyplot as plt
from pathlib import Path

FFT_LEN = 1024   #Padded with zeros if longer than data window size 
MAX_FREQ = 5000  #Maximum frequency to disply in spectrogram

data_names = ["pride_and_prejudice_part1.wav", "white_fang_part1.wav"]
data_path = Path("data")

def read_soundfile(fname):
    '''Reads a wave file and returns the sample rate and samples'''
    data, rate = sf.read(fname, start=0, stop=None, dtype="float64")
    print(len(data),rate)
    return data, rate

def plot_sound(wav1, wav2, fs1, fs2, title1, title2):
    '''This plot uses fig and axis objects'''
    #Use linspace to create a time axis
    #1/fs * len(wav) gives length of time in seconds
    timeaxis1 = np.linspace(0, 1/fs1*len(wav1), len(wav1))  #Use linspace here
    timeaxis2 = np.linspace(0, 1/fs2*len(wav2), len(wav2))  #Use linspace here
    fig, ax = plt.subplots(nrows=2,figsize=(12,4))  #Use plt.subplots with nrows = 2; optionally use figsize
    ax[0].plot(timeaxis1, wav1) #Call ax[0].plot
    ax[1].plot(timeaxis2, wav2) #Call ax[1].plot
    #Set the title for each ax
    fig.tight_layout()
    plt.show()  #Show the plot

def show_window(win_type, win_len):
    '''Display a signal analysis window - hamming, hanning, etc'''
    w = win_type(win_len)
    fig, ax = plt.subplots(figsize = (12, 4))
    ax.plot(w)
    plt.show()

def enframe(x, skip_len, win_len):
    '''Splits audio into frames, multplies by a window; returns
       list of windowed frames'''
    print(f"skip_len: {skip_len}, win_len: {win_len}")
    w = np.hamming(win_len)  #Win type ould be an argument
    frames = []
    nframes = []
    nframes = 1 + int((len(x) -win_len)/skip_len)
    for t in range(0,nframes):
        frames.append(np.copy(x[(t*skip_len): (t*skip_len+win_len)])*w)
    return frames

def test_frames(wav1, wav2, fs1, fs2, title1, title2):
    '''Plots one frame from each sound as a check'''
    print(f"fs1: {fs1}, fs2: {fs2}")
    #skip len is 100 ms, window len 350 ms
    w1_frames = enframe(wav1, int(0.01*fs1), int(0.035*fs1))
    w2_frames = enframe(wav2, int(0.01*fs2), int(0.035*fs2))
    fig, ax = plt.subplots(nrows = 2, figsize = (14, 4))
    ax[0].plot(np.linspace(0, 0.005, len(w1_frames[11])), w1_frames[11])
    ax[0].set_title(title1)
    ax[1].plot(np.linspace(0, 0.005, len(w2_frames[11])), w2_frames[11])
    ax[1].set_title(title2)
    fig.tight_layout()
    plt.show()

def test_stft(wav1, wav2, fs1, fs2, title1, title2):
    '''Calculate magnitude-squared stft of one frame of each wav'''
    w1_frames = enframe(wav1, int(0.01*fs1), int(0.035*fs2))
    w2_frames = enframe(wav2, int(0.01*fs2), int(0.035*fs2))
    w1_stft, w1_freqaxis = stft(w1_frames, FFT_LEN, fs1)
    w2_stft, w2_freqaxis = stft(w2_frames, FFT_LEN, fs2)
    plot_stft(w1_stft, w1_freqaxis, w2_stft, w2_freqaxis, title1, title2)

def plot_stft(w1_stft, w1_freqaxis, w2_stft, w2_freqaxis, title1, title2):
    '''Displays stft of one frame; source article version 2
       This version only plots frequencies to 5 kHz'''
    fig, ax = plt.subplots(nrows = 2, figsize = (12, 4))
    ax[0].plot(w1_freqaxis[w1_freqaxis<=MAX_FREQ],
               np.log(abs(w1_stft[11][w1_freqaxis<=MAX_FREQ])))
    #ax[1].plot(w2_freqaxis, np.log(np.maximum(1, abs(w2_stft[11])**2)))
    ax[1].plot(w2_freqaxis[w2_freqaxis<=MAX_FREQ],
               np.log(abs(w2_stft[11][w2_freqaxis<=MAX_FREQ])))
    ax[0].set_ylabel("Magnitude Squared STFT")
    ax[1].set_ylabel("Magnitude Squared STFT")
    ax[0].set_title(title1)
    ax[1].set_title(title2)
    ax[0].set_xlabel("Frequency (Hertz)")
    ax[1].set_xlabel("Frequency (Hertz)")
    fig.tight_layout()
    plt.show()

def stft(frames, fft_len, fs):
    '''Returns fft of frames and frequency axis
       Uses scipy rfft and rfftfreq'''
    stft_frames = [scipy.fft.rfft(x, n=fft_len) for x in frames]  #Write code to call scipy.rfft over the frames...
    #...creating a list of stft_frames
    #stft_frames is a list of ndarrays
    freqs = scipy.fft.rfftfreq(fft_len, 1/fs) #Get a list of fft freq bins
    print(freqs)
    return stft_frames, freqs

def stft2level(stft_spectra, max_freq_bin):
    '''Converts spectrum to decibels; finds highest magnitude pixel then
    make sure every pixel >= 1/1000 of highest (60dB down) - this ensures
    we won't get a negative infinity value; take log of values'''
    magnitude_spectra = [np.abs(x) for x in stft_spectra]
    max_magnitude = max([max(x) for x in magnitude_spectra])
    min_magnitude = max_magnitude/1000
    for t in range(0, len(magnitude_spectra)):
        for k in range(0, len(magnitude_spectra[t])):
            magnitude_spectra[t][k] /= min_magnitude
            if magnitude_spectra[t][k] < 1:
                magnitude_spectra[t][k] = 1
    level_spectra = [20*np.log10(x[0:max_freq_bin]) for x in magnitude_spectra]
    return level_spectra

def sgram(x, frame_skip, frame_length, fft_length, fs, max_freq):
    frames = enframe(x,frame_skip, frame_length)  #Get a list of windowed frames
    spectra, freq_axis = stft(frames, fft_length, fs)  #Use stft
    sgram = stft2level(spectra, int(max_freq * fft_length/fs))  #Set the levels on the spectra and convert to log dB
    max_time = len(frames) * frame_skip/fs
    return sgram, max_time, max_freq

def show_spect(sgram_data, maxtime, maxfreq, xlabel, ylabel, title):
    fig, ax = plt.subplots(figsize=(12, 4))  #Use plt.subplots
    ax.imshow(np.transpose(np.array(sgram_data)), origin = "lower",
              extent = (0, maxtime, 0, maxfreq), aspect = "auto")
    #Set x_label, y_label, and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.show()

def main():
    p_data, p_fs = read_soundfile(data_path/data_names[0])  #Read the sound file for data_names[0]
    w_data, w_fs = read_soundfile(data_path/data_names[1])  #Read the sound file for data_names[1]
    #Cut out 0.6 sec segment from each sound...
    #...Start at 0.74 sec for p_data, 0.42 sec for w_data
    p_wav = p_data[int(0.74 * p_fs) : int((0.74 + 0.6) * p_fs)] #small segment of wav files
    w_wav = w_data[int(0.42 * w_fs) : int((0.42 + 0.6) * w_fs)]

    #Play the sounds; use sd.play() and sd.wait()
    sd.play(p_wav)
    sd.wait()
    sd.play(w_wav) 
    sd.wait()       
    plot_sound(p_wav, w_wav, p_fs, w_fs,
               "First segment from Pride and Prejudice",
               "First segment from White Fang")
    test_frames(w_wav, p_wav, w_fs, p_fs, "A frame from White Fang",
                "A frame from Pride and Prejudice")
    test_stft(w_wav, p_wav, w_fs, p_fs, "Spectrum of a frame from White Fang",
              "Spectrum of a frame from Pride and Prejudice")
    p_frames = enframe(p_wav, int(0.01*p_fs), int(0.035*p_fs))
    p_stft, freq_axis = stft(p_frames, FFT_LEN, p_fs)
    p_sgram, p_maxtime, p_maxfreq = sgram(p_wav, int(.009 * p_fs),
            int(0.035 * p_fs), FFT_LEN, p_fs, MAX_FREQ)
    show_spect(p_sgram, p_maxtime, p_maxfreq, "Time (ms)", "Frequency (Hz)",
               "Narrowband Spectrogram of a segment from Pride and Prejudice")
    #Wideband spectrogram
    p_sgram, p_maxtime, p_maxfreq = sgram(p_wav, int(0.001 * p_fs),
                        int(0.004 * p_fs), FFT_LEN, p_fs, MAX_FREQ)
    show_spect(p_sgram, p_maxtime, p_maxfreq, "Time (ms)", "Frequency (Hz)",
        "Wideband Spectrogram of a segment from Pride and Prejudice")
    w_sgram, w_maxtime, w_maxfreq = sgram(w_wav, int(0.001 * w_fs),
                        int(0.004 * w_fs), FFT_LEN, w_fs, MAX_FREQ)
    show_spect(w_sgram, w_maxtime, w_maxfreq, "Time (ms)", "Frequency (Hz)",
        "Wideband Spectrogram of a segment from White Fang")
    nbw_sgram, w_maxtime, w_maxfreq = sgram(w_wav, int(0.009 * w_fs),
                        int(0.035 * w_fs), FFT_LEN, w_fs, MAX_FREQ)
    show_spect(nbw_sgram, w_maxtime, w_maxfreq, "Time (ms)", "Frequency (Hz)",
        "Narrowband Spectrogram of a segment from White Fang")

main()
#Comment out call to main when looking at windows
#show_window(np.hamming, 200)  #Others: blackman, hanning, bartlett
        
