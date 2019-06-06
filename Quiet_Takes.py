# Feature extraction example
import numpy as np
import librosa
import wave

# Load the example clip

film_name = "The_Silence.wav"
the_clip, sr = librosa.load(film_name)

num_samps = len(the_clip)

print(sr)

# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length_1 = 128
frame_hop_ratio = 2



rms_vals1 = librosa.feature.rms(the_clip, frame_length= (frame_hop_ratio * hop_length_1), hop_length=hop_length_1)

print("RMS max: " + str(max(rms_vals1[0])))
print("RMS min: " + str(min(rms_vals1[0])))

List_of_Labels = []

startpoint = 0
in_recording = False

min_seconds_for_record = 4
min_windows_for_record = (sr * min_seconds_for_record)/(hop_length_1)

RMS_max = 0.03


for index in range(len(rms_vals1[0])):
    if in_recording:
        if (rms_vals1[0][index] > RMS_max) | (index == len(rms_vals1[0])):
            if (index - startpoint) >= min_windows_for_record:
                List_of_Labels.append(str(((startpoint + 2) * hop_length_1)/float(sr)) + "\t" +
                                          str(((index - 2) * hop_length_1)/float(sr)) + "\t" +
                                          str(np.mean(rms_vals1[0][startpoint + 2 : index - 2])) + "\n")
                in_recording = False
                startpoint = index
            else:
                startpoint = index
    else:
        if rms_vals1[0][index] < RMS_max:
            startpoint = index
            in_recording = True

print(len(List_of_Labels))

QTLs = open(film_name + "_Labels.txt", "w")

for label_index in List_of_Labels:
    QTLs.write(label_index)

QTLs.close()
