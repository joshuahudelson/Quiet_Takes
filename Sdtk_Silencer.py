# Sdtk_Silencer

import numpy as np
import scipy.io.wavfile


class Sdtk_Silencer:
    """ Whatever it is.
    """

    def __init__(self, wavefile,
                 window_width = 5000,
                 hop_size = 5,
                 min_silence_samples = 130000,
                 rms_threshold = 0.01):

        self.filename = wavefile
        self.raw = scipy.io.wavfile.read(wavefile)[1]/float(32768)
        self.rawlen = len(self.raw)

        self.window_width = window_width
        self.hop_size = hop_size
        self.min_silence_samples = min_silence_samples
        self.rms_threshold = rms_threshold
        self.in_loop = None

        self.silence_labels = []

    def get_rms(self, segment):
        return np.sqrt(np.mean(np.square(segment)))

    def generate_silence_labels(self):

        self.in_loop = False
        start_point = None
        end_point = None

        for hop in range(int((self.rawlen - self.window_width) / self.hop_size)):

            windowstart = hop * self.hop_size
            current_segment = self.raw[windowstart:windowstart + self.window_width]

            RMS = self.get_rms(current_segment)

            if RMS < self.rms_threshold:
                if self.in_loop:
                    pass
                else:
                    self.in_loop = True
                    start_point = (hop * self.hop_size)
            else:
                if self.in_loop:
                    if ((hop * self.hop_size) - start_point) >= self.min_silence_samples:
                        end_point = ((hop - 1) * self.hop_size)
                        self.silence_labels.append([start_point, end_point])
                        start_point = None
                        end_point = None
                        self.in_loop = False
                    else:
                        start_point = None
                        end_point = None
                        self.in_loop = False

        if self.in_loop:
            end_point = self.rawlen
            if start_point - end_point >= self.min_silence_samples:
                self.silence_labels.append([start_point, end_point])

        return(self.silence_labels)

    def export_text_file(self):
        textfile = open(self.filename + "_Labels", "w")
        for entry in self.silence_labels:
            textfile.write(str(entry[0]/float(44100)) + "\t" + str(entry[1]/float(44100)) + "\n")
        textfile.close()

if __name__== '__main__':
    myvar = Sdtk_Silencer("SilenceTenMono.wav")
    myvar.generate_silence_labels()
    myvar.export_text_file()
