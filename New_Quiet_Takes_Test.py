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
hop_length_2 = 2*hop_length_1
hop_length_3 = 8*hop_length_1


rms_vals1 = librosa.feature.rms(the_clip, frame_length=hop_length_1, hop_length=hop_length_1)
flat_vals1 = librosa.feature.spectral_flatness(the_clip, n_fft=hop_length_1, hop_length=hop_length_1)

rms_vals2 = librosa.feature.rms(the_clip, frame_length=hop_length_2, hop_length=hop_length_2)
flat_vals2 = librosa.feature.spectral_flatness(the_clip, n_fft=hop_length_2, hop_length=hop_length_2)

rms_vals3 = librosa.feature.rms(the_clip, frame_length=hop_length_3, hop_length=hop_length_3)
flat_vals3 = librosa.feature.spectral_flatness(the_clip, n_fft=hop_length_3, hop_length=hop_length_3)


textfile1 = open("RMS1_Labels.txt", "w")
textfile2 = open("RMS2_Labels.txt", "w")
textfile3 = open("RMS3_Labels.txt", "w")

flatfile1 = open("FLAT1_Labels.txt", "w")
flatfile2 = open("FLAT2_Labels.txt", "w")
flatfile3 = open("FLAT3_Labels.txt", "w")

for count, entry in enumerate(rms_vals1[0]):
    textfile1.write(str((count * hop_length_1)/float(sr)) + "\t" +
               str(((count+1)*hop_length_1)/float(sr)) + "\t" +
               str(entry) + "\n")
textfile1.close()

for count, entry in enumerate(flat_vals1[0]):
    flatfile1.write(str((count * hop_length_1)/float(sr)) + "\t" +
               str(((count+1)*hop_length_1)/float(sr)) + "\t" +
               str(entry) + "\n")
flatfile1.close()

#-----

for count, entry in enumerate(rms_vals2[0]):
    textfile2.write(str((count * hop_length_2)/float(sr)) + "\t" +
               str(((count+1)*hop_length_2)/float(sr)) + "\t" +
               str(entry) + "\n")
textfile2.close()

for count, entry in enumerate(flat_vals2[0]):
    flatfile2.write(str((count * hop_length_2)/float(sr)) + "\t" +
               str(((count+1)*hop_length_2)/float(sr)) + "\t" +
               str(entry) + "\n")
flatfile2.close()

#-----

for count, entry in enumerate(rms_vals3[0]):
    textfile3.write(str((count * hop_length_3)/float(sr)) + "\t" +
               str(((count+1)*hop_length_3)/float(sr)) + "\t" +
               str(entry) + "\n")
textfile3.close()

for count, entry in enumerate(flat_vals3[0]):
    flatfile3.write(str((count * hop_length_3)/float(sr)) + "\t" +
               str(((count+1)*hop_length_3)/float(sr)) + "\t" +
               str(entry) + "\n")
flatfile3.close()
