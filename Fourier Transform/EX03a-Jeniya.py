'''CSC 745 Advanced Multimedia Programming
Exercise: Experiment with the Fourier transform
Name: Jeniya Sultana
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import sounddevice as sd

MAX_INT16 = 32767
INT16_DTYPE = "int16"

# Function to generate a sine wave
def generate_sine_wave(freq, dur, rate):
    t = np.linspace(0, dur, dur*rate, endpoint= False)
    s = np.sin((2*np.pi)*freq*t)
    return t,s

# Function to plot a sound wave
def plot_sound_wave(t, sig, rate, title):
    duration = len(sig)/rate
    fig, ax = plt.subplots()
    ax.plot(t, sig)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    plt.show()

# Funcrtion to mix sound wave
def mix_sound_wave(*waves):
    mixed_wave = np.zeros(len(waves[0]), dtype = np.float32)
    for wave in waves:
        mixed_wave += wave
    mixed_wave /= len(waves)
    return mixed_wave

# Function to scale mixed signal
def scale_signal(signal, target_value, data_type):
    scale_factor = target_value/np.abs(signal).max()
    new_signal = np.array(signal*scale_factor, dtype = data_type)
    return new_signal

# Function to generate spectrum
def generate_specturm(signal, rate, real):
    N = len(signal)
    if real == True:
        spectrum = rfft(signal)
        frequency =rfftfreq(N, 1/rate)
    else:
        spectrum = fft(signal)
        frequency = fftfreq(N, 1/rate)
    return frequency, spectrum

# Function to plot spectrum
def plot_spectrum(frequency, spectrum, title):
    fig, ax = plt.subplots()
    ax.plot(frequency, np.abs(spectrum))
    ax.set_xlabel("frequency in Hz")
    ax.set_ylabel("Magnitude")
    ax.set_title(title)
    plt.show()


def main():
    sample_rate = 8000
    duration = 2
    amplitude = MAX_INT16
    frequency1 = 100

    # Plotting 1 cycle
    t, sine_wave1 = generate_sine_wave(frequency1, duration, sample_rate)
    num_samples = sample_rate//frequency1 * 1
    plot_sound_wave(t[:num_samples], sine_wave1[:num_samples], sample_rate, f"{frequency1} Hz (1 cycle)")

    # Plotting 5 cycle wave
    num_samples = sample_rate//frequency1 * 5
    plot_sound_wave(t[:num_samples], sine_wave1[:num_samples], sample_rate, f"{frequency1} Hz (5 cycles)")

    sd.play(sine_wave1, sample_rate)
    sd.wait()

    frequency2 = 3000

    # generating sine wave and amplitude modification
    t, sine_wave2 = generate_sine_wave(frequency2, duration, sample_rate)
    sine_wave2 *= 0.3

    # mixing waves
    mix_wave = mix_sound_wave(sine_wave1, sine_wave2)
    scaled_wave = scale_signal(mix_wave, MAX_INT16, INT16_DTYPE)

    # plotting mixed waved and then scaled wave
    plot_sound_wave(t[:num_samples], mix_wave[:num_samples], sample_rate, f"{frequency1} Hz + {frequency2} Hz (Mixed Wave)")
    plot_sound_wave(t[:num_samples], scaled_wave[:num_samples], sample_rate, f"{frequency1} Hz + {frequency2} Hz (Scaled)")

    sd.play(mix_wave, sample_rate)
    sd.wait()

    # spectrum generation and plotting
    num_samples = sample_rate//100
    frequency, spectrum = generate_specturm(scaled_wave[:num_samples], sample_rate, real=False)
    plot_spectrum(frequency, spectrum, "Using fft and fftfreq")

    frequency, spectrum = generate_specturm(scaled_wave[:num_samples], sample_rate, real=True)
    plot_spectrum(frequency, spectrum, "Using rfft and rfftfreq")

main()