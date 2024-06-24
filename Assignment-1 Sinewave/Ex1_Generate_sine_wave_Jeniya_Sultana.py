'''CSC 745 Advanced Multimedia Programming
Exercise: Generate and plot a sine wave
Name: Jeniya Sultana
'''


# Step 2: Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# function for generating sine wave using signal = 2*pi*freq*time
def generate_sine_wave(frequency, time, amplitude = 1):
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * time)
    return sine_wave

def time_generation(duration, sample_rate):
    # Create a linear array of time values
    # time = np.arange(0, duration, 1/sample_rate) #np.arange([start], stop, [step])
    time = np.linspace(0, duration, duration*sample_rate, endpoint=False)
    return time

# function for plotting sine wave
def plot_wave(time, sine_wave, text):
    plt.figure(figsize=(10, 4))
    plt.plot(time, sine_wave)
    plt.title(text)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

# variables
# Step 3: Generate a sine wave at 10 Hz, sampled at 100 Hz
frequency = 10  # Hz
sample_rate = 100  # Hz
duration = 2  # seconds
amplitude = 1.0

# time and sine wave generation
time = time_generation(duration, sample_rate)
sine_wave = generate_sine_wave(frequency, time)

# Print some sample values
print("Some sample values", sine_wave[:10])

# Step 4: Plot the wave – you should see 20 cycles (2 sec * 10 Hz)
output_filename = "sine_wave_10Hz.wav"
write(output_filename, sample_rate, sine_wave.astype(np.int16))
plot_wave(time,sine_wave,"Sine Wave at 10 Hz")

# Step 5: Generate 3 seconds and plot – you should see 30 cycles
duration = 3  # seconds
time = time_generation(duration, sample_rate)
sine_wave = generate_sine_wave(frequency, time)

output_filename = "sine_wave_10Hz_3sec.wav"
write(output_filename, sample_rate, sine_wave.astype(np.int16))
plot_wave(time, sine_wave, "Sine wave at 10 Hz for 3 Seconds")

# Step 6: Plot one cycle
time = time_generation(duration, sample_rate)
sine_wave = generate_sine_wave(frequency, time)
samples = int(sample_rate/frequency)

output_filename = "sine_wave_10Hz_1cycle.wav"
write(output_filename, sample_rate, sine_wave.astype(np.int16))
plot_wave(time[:samples], sine_wave[:samples], "One Cycle of Sine Wave at 10 Hz")

# Step 7: Change your frequency to 440 Hz, sample rate to 800 Hz, and amplitude to 127 (8 bit samples)
frequency = 440  # Hz
sample_rate = 800  # Hz
amplitude = 127

# Step 8: Generate and plot the wave
duration = 1  # second
time = time_generation(duration, sample_rate)
sine_wave = generate_sine_wave(frequency, time, amplitude)

output_filename = "sine_wave_440Hz_8bit.wav"
write(output_filename, sample_rate, sine_wave.astype(np.int16))
plot_wave(time, sine_wave, "Sine Wave at 440 Hz (8-bit)")

# Step 9: Plot 1 cycle for the new settings
sample_rate = 8000 # Hz
time = time_generation(duration, sample_rate)
sine_wave = generate_sine_wave(frequency, time, amplitude)
samples = int(sample_rate/frequency)

output_filename = "sine_wave_440Hz.wav"
write(output_filename, sample_rate, sine_wave.astype(np.int16))
plot_wave(time[:samples], sine_wave[:samples], "One Cycle of Sine Wave at 440 Hz")

# Step 11: Write the sound to a file
# written while plotting

# Step 12: Open Audacity or another audio editor, load and play the sound.
# Zoom in closely to see its shape.

# Step 13: Experiment with sine waves and generate 2 or 3 waves and add them together.
# Be sure not to exceed your amplitude range.
# One experiment sample

# sample_rate = 800
# duration = 3
# frequency1 = 440
# frequency2= 880
# amplitude = 32767
# time = time_generation(duration, sample_rate)
# added_sine_wave = generate_sine_wave(frequency1, time) + generate_sine_wave(frequency2, time)
# plot_wave(time+time, added_sine_wave, "Added Sine wave")
# output_filename = "added_sine_wave.wav"
# write(output_filename, sample_rate, added_sine_wave.astype(np.int16))