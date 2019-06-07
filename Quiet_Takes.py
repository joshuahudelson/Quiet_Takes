# Feature extraction example
import numpy as np
import librosa
import wave
import os

# Load the example clip

film_name = "Clip1.wav"
the_clip, sr = librosa.load(film_name)

num_samps = len(the_clip)

print(sr)

# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length_rms = 128
frame_hop_ratio_rms = 2

frame_length_rms = frame_hop_ratio_rms * hop_length_rms

hop_length_flat = 512
frame_hop_ratio_flat = 2

frame_length_flat = frame_hop_ratio_flat * hop_length_flat

rms_to_flat_hop_ratio = hop_length_rms/hop_length_flat

rms_vals1 = librosa.feature.rms(the_clip, frame_length=frame_length_rms, hop_length=hop_length_rms)
flat_vals1 = librosa.feature.spectral_flatness(the_clip, n_fft=frame_length_flat, hop_length=hop_length_flat)

List_of_Labels = []

print("RMS max: " + str(max(rms_vals1[0])))
print("RMS min: " + str(min(rms_vals1[0])))

print("FLAT max: " + str(max(flat_vals1[0])))
print("FLAT min: " + str(min(flat_vals1[0])))

startpoint = 0
in_recording = False

min_seconds_for_record = 2
min_windows_for_record = (sr * min_seconds_for_record)/(hop_length_rms)


RMS_max = 0.03
FLAT_min = 0.005


for index in range(len(rms_vals1[0])):
    if in_recording:
        if (rms_vals1[0][index] > RMS_max) | (flat_vals1[0][int(rms_to_flat_hop_ratio * index)] < FLAT_min) | (index == len(rms_vals1[0])):
            if (index - startpoint) >= min_windows_for_record:
                List_of_Labels.append(str(((startpoint + 2) * hop_length_rms)/float(sr)) + "\t" +
                                          str(((index - 2) * hop_length_rms)/float(sr)) + "\t" +
                                          str(np.mean(rms_vals1[0][startpoint + 2 : index - 2])) + "\n")
                in_recording = False
                startpoint = index
            else:
                startpoint = index
        else:
            continue # rms and flatness are still good, recording continues...
    else:
        if (rms_vals1[0][index] < RMS_max) & (flat_vals1[0][int(rms_to_flat_hop_ratio * index)] > FLAT_min):
            startpoint = index
            in_recording = True

print(len(List_of_Labels))

try:
    os.mkdir(film_name + "_Final_Labels")
except FileExistsError:
    print("Directory already exists.")

cwd = os.getcwd()

directory_name = cwd + str("/") + film_name + "_Final_Labels"

print(directory_name)

QTLs = open(directory_name + str("/") + film_name + "_Final_Labels.txt", "w")

for label_index in List_of_Labels:
    QTLs.write(label_index)

QTLs.close()
