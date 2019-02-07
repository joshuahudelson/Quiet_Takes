# Sdtk_Silencer

import numpy as np
import scipy.io.wavfile


class Sdtk_Silencer:
    """ Whatever it is.
    """

    def __init__(self, wavefile,
                 window_width = 10000,
                 hop_size = 50,
                 min_silence_samples = 130000,
                 rms_threshold = 0.008,
                 maxamp = 0.4):

        self.filename = wavefile
        self.raw = scipy.io.wavfile.read(wavefile)[1]/float(32768)
        self.rawlen = len(self.raw)
        self.maxamp = maxamp

        self.window_width = window_width
        if hop_size > window_width:
            print("Hop size truncated to window width!")
            self.hop_size = window_width
        else:
            self.hop_size = hop_size
        self.min_silence_samples = min_silence_samples
        self.rms_threshold = rms_threshold
        self.in_loop = None

        self.silence_labels = []

    def get_rms(self, segment):
        return np.sqrt(np.mean(segment))

    def generate_silence_labels(self):

        self.in_loop = False
        start_point = None
        end_point = None

        current_segment = self.raw[0:self.window_width]
        current_seg_square = np.square(current_segment)

        TotalRMS = 0
        Divisor = 0

        for hop in range(int((self.rawlen - self.window_width) / self.hop_size)):

            RMS = self.get_rms(current_seg_square)

            if (RMS < self.rms_threshold) & (np.amax(current_seg_square) < self.maxamp):
                if self.in_loop:
                    TotalRMS += RMS
                    Divisor += 1
                else:
                    self.in_loop = True
                    start_point = (hop * self.hop_size)
            else:
                if self.in_loop:
                    if ((hop * self.hop_size) - start_point) >= self.min_silence_samples:
                        end_point = ((hop - 1) * self.hop_size)
                        self.silence_labels.append([start_point, end_point, TotalRMS/Divisor])
                        start_point = None
                        end_point = None
                        self.in_loop = False
                        TotalRMS = 0
                        Divisor = 0
                    else:
                        start_point = None
                        end_point = None
                        self.in_loop = False
                        TotalRMS = 0
                        Divisor = 0
                else:
                    pass

            current_seg_square = current_seg_square[self.hop_size:]
            x = ((hop + 1) * self.hop_size) + (self.window_width - self.hop_size)
            newvalues = self.raw[x : (x + self.hop_size)]
            newvalues_square = np.square(newvalues)
            current_seg_square = np.concatenate((current_seg_square, newvalues_square), axis=0)

        if self.in_loop:
            end_point = self.rawlen
            if start_point - end_point >= self.min_silence_samples:
                self.silence_labels.append([start_point, end_point, TotalRMS/Divisor])

        return(self.silence_labels)

    def export_text_file(self):
        textfile = open(self.filename[:-4] + "_Labels.txt", "w")
        for entry in self.silence_labels:
            textfile.write(str(entry[0]/float(44100)) + "\t" + str(entry[1]/float(44100)) + "\t" + str(entry[2]) + "\n")
        textfile.close()

if __name__== '__main__':
    myvar = Sdtk_Silencer("BergmanSilence.wav")
    myvar.generate_silence_labels()
    myvar.export_text_file()
