import librosa
import soundfile as sf
# from scipy.signal import medfilt

x, sr = librosa.load('raw.wav', sr=None)

har_, per_ = librosa.effects.hpss(x)
clean_x = har_


sf.write('clean_audio.wav', clean_x, sr)

print("Background noise reduced!")