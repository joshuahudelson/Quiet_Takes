# Feature extraction example
import numpy as np
import librosa
import wave

# Load the example clip
the_clip, sr = librosa.load("silenceclip1.wav")

num_samps = len(the_clip)

print(sr)

# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length_1 = 512
#hop_length_2 = 2*hop_length_1
#hop_length_3 = 8*hop_length_1


rms_vals1 = librosa.feature.rms(the_clip, frame_length=hop_length_1, hop_length=hop_length_1)
flat_vals1 = librosa.feature.spectral_flatness(the_clip, n_fft=hop_length_1, hop_length=hop_length_1)

print("RMS max: " + str(max(rms_vals1[0])))
print("RMS min: " + str(min(rms_vals1[0])))
print("FLAT max: " + str(max(flat_vals1[0])))
print("FLAT min: " + str(min(flat_vals1[0])))

#rms_vals2 = librosa.feature.rms(the_clip, frame_length=hop_length_2, hop_length=hop_length_2)
#flat_vals2 = librosa.feature.spectral_flatness(the_clip, n_fft=hop_length_2, hop_length=hop_length_2)

#rms_vals3 = librosa.feature.rms(the_clip, frame_length=hop_length_3, hop_length=hop_length_3)
#flat_vals3 = librosa.feature.spectral_flatness(the_clip, n_fft=hop_length_3, hop_length=hop_length_3)


Quiet_Takes_Labels = []

startpoint = 0
in_recording = False
min_windows_for_record = 100

RMS_max = 0.05
FLAT_min = 0.005


for index in range(len(rms_vals1[0])):
    if in_recording:
        if (rms_vals1[0][index] > RMS_max) | (index == len(rms_vals1[0])):
            if (index - startpoint) >= min_windows_for_record:
                Quiet_Takes_Labels.append(str((startpoint * hop_length_1)/float(sr)) + "\t" + str((index * hop_length_1)/float(sr)) + "\t" + str(np.mean(rms_vals1[0][startpoint:index])) + "\n")
                in_recording = False
                startpoint = index
            else:
                startpoint = index
    else:
        if rms_vals1[0][index] < RMS_max:
            startpoint = index
            in_recording = True

print(len(Quiet_Takes_Labels))

QTLs = open("Quiet_Takes_Labels.txt", "w")

for label_index in Quiet_Takes_Labels:
    QTLs.write(label_index)

QTLs.close()
