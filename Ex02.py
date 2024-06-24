from scipy.io import wavfile
import sounddevice as sd
fname_speech = "OSR_us_000_0010_8K.wav"


def read_wav(fname):
    '''Read a wave file and return sample rate and sampled data'''
    rate, samples = wavfile.read(fname)
    return rate, samples

def diff_samples(sig):
    '''Return differentiated signal'''
    new_sig = np.array([sign[i]-sig[i-1] for i in range(1,len(sig))],
                       dtype=sig.dtype)
    return new_sig

def main():
    fs, data = read_wav(fname_speech)
    print(fs, len(data), max(abs(data)), len(data)/fs)
    sd.play(data[:40000], fs)
    sd.wait()
    diff_data = diff_samples(data)
    sd.play(diff_data, fs)
    sd.wait()