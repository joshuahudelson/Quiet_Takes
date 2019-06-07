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

# Set the hop length (at 22050 Hz, 512 samples ~= 23ms)
hop_length_rms = 128
frame_hop_ratio_rms = 2

frame_length_rms = frame_hop_ratio_rms * hop_length_rms

hop_length_flat = 512
frame_hop_ratio_flat = 2

frame_length_flat = frame_hop_ratio_flat * hop_length_flat

rms_vals1 = librosa.feature.rms(the_clip, frame_length=frame_length_rms, hop_length=hop_length_rms)
flat_vals1 = librosa.feature.spectral_flatness(the_clip, n_fft=frame_length_flat, hop_length=hop_length_flat)

RMS_Labels = []
FLAT_Labels = []

for index in range(len(rms_vals1[0])):

    temp_start_point = str((index * hop_length_rms)/float(sr))
    temp_end_point = str(((index + 1) * hop_length_rms)/float(sr))

    RMS_Labels.append(temp_start_point + "\t" +
                      temp_end_point + "\t" +
                      str(rms_vals1[0][index]) + "\n")


for index in range(len(flat_vals1[0])):

    temp_start_point = str((index * hop_length_flat)/float(sr))
    temp_end_point = str(((index + 1) * hop_length_flat)/float(sr))

    FLAT_Labels.append(temp_start_point + "\t" +
                       temp_end_point + "\t" +
                       str(flat_vals1[0][index]) + "\n")
try:
    os.mkdir(film_name + "_RMS_and_FLAT_Analyses")
except FileExistsError:
    print("Directory already exists.")

cwd = os.getcwd()

directory_name = cwd + str("/") + film_name + "_RMS_and_FLAT_Analyses"

print(directory_name)

RMSLs = open(directory_name + str("/") + film_name + "_RMS_Labels.txt", "w")
FLATLs = open(directory_name + str("/") + film_name + "_FLAT_Labels.txt", "w")

for entry in RMS_Labels:
    RMSLs.write(entry)
RMSLs.close()

for entry in FLAT_Labels:
    FLATLs.write(entry)
FLATLs.close()
