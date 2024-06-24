import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# Sample data for demonstration
# You can replace this with your own frequency domain data
sample_rate = 1000  # Sampling rate in Hz
duration = 1.0  # Duration of the signal in seconds
frequency = 5.0  # Frequency of the signal in Hz

# Generate a sine wave in the frequency domain
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal_frequency_domain = np.fft.fft(np.sin(2 * np.pi * frequency * t))
sd.play(t, sample_rate)
sd.wait()

sd.play(signal_frequency_domain, sample_rate)
sd.wait()


# Perform the inverse FFT to obtain the time domain signal
signal_time_domain = np.fft.ifft(signal_frequency_domain)

sd.play(signal_time_domain, sample_rate)
sd.wait()

# Plot the original signal and the reconstructed signal
plt.figure(figsize=(10, 4))

# Original signal (time domain)
plt.subplot(2, 1, 1)
plt.plot(t, np.sin(2 * np.pi * frequency * t))
plt.title("Original Signal (Time Domain)")

# Reconstructed signal (time domain)
plt.subplot(2, 1, 2)
plt.plot(t, signal_time_domain)
plt.title("Reconstructed Signal (Time Domain)")

plt.tight_layout()
plt.show()
