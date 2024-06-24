'''CSC 745 Advanced Multimedia Programming
Exercise: Differentiation
Name: Jeniya Sultana'''

#import librarires
import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal

#read file
sample_rate, data = wavfile.read('OSR_us_000_0015_8k.wav')

#print relevant value
print(f"Sample rate: {sample_rate}")
print(f"Number of sample: {len(data)}")
print(f"Maximum sample value: {np.max(np.abs(data))}")
duration = len(data)/sample_rate
print(f"Duration (seconds): {duration}")

# play the sound
sd.play(data, sample_rate)
sd.wait()

# creating a new array with differences of samples
differenced_samples = np.diff(data)

# playing both arrays
sd.play(data, sample_rate)
sd.wait()
sd.play(differenced_samples, sample_rate)
sd.wait()

print(f"Maximum sample value in differenced array: {np.max(np.abs(differenced_samples))}")

# scaling audio data
scaled_data = differenced_samples/np.max(np.abs(differenced_samples))

# plotting both arrays
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.plot(data)
plt.title("Original data")
plt.subplot(2,1,2)
plt.plot(differenced_samples)
plt.title("Differenced data")
plt.subplots_adjust(hspace=0.4)  
plt.show()

# writing scaled data
wavfile.write("differenced_sound_file.wav", sample_rate, scaled_data)

# loading scaled data
loaded_wav_file = wavfile.read("differenced_sound_file.wav")[1] #[1] returns the data
sd.play(loaded_wav_file, sample_rate)
sd.wait()

# plotting scaled data
plt.plot(loaded_wav_file)
plt.title("Reloaded scaled data")
plt.show()

# generating spectrogram of both arrays
frequencies_original, times_original, sxx_original = signal.spectrogram(data[16000:40000], fs=sample_rate)
frequencies_differenced, times_differenced, sxx_differenced = signal.spectrogram(differenced_samples[16000:40000], fs = sample_rate)

# plotting spectrograms
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.pcolormesh(times_original, frequencies_original, sxx_original, shading='gouraud')
plt.title("Spectrogram of original sound wave")
plt.subplot(2,1,2)
plt.pcolormesh(times_differenced, frequencies_differenced, sxx_differenced, shading='gouraud')
plt.title("Spectrogram of differenced wave")
plt.subplots_adjust(hspace=0.4)  
plt.show()

# increasing amplitude
data *= 10
differenced_samples *= 10

# printing max values
print(f"Max value in original data (amplified): {np.max(np.abs(data))}")
print(f"Max value in differenced data (amplified): {np.max(np.abs(differenced_samples))}")

# plotting amplified waveforms
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
plt.plot(data)
plt.title("Amplified original data")
plt.subplot(2,1,2)
plt.plot(differenced_samples)
plt.title("Amplified differenced data")
plt.subplots_adjust(hspace=0.4)  
plt.show()
