# Sdtk_Silencer

import numpy as np
import scipy.io.wavfile


class Sdtk_Silencer:
    """ Whatever it is.
    """

    def __init__(self,
                 wavefile,
                 min_samples = 150000,
                 ):

        self.filename = wavefile
        self.raw = scipy.io.wavfile.read(wavefile)[1]/float(32768)
        self.rawlen = len(self.raw)

        self.maxamp = maxamp

        self.min_samples = min_samples

        self.subsegment_percentages = subsegment_percentages
        self.rms_ratios = rms_ratios
        self.hopsize_percentages = hopsize_percentages

        self.in_loop = None
        self.silence_labels = []


    def run_analysis(self):
        level = 0
        hopsize = self.min_samples * hopsize_percentages[level]
        num_hops = ((self.rawlen - self.min_samples) / hopsize) + 1
        start_point = 0
        for hop in range(num_hops):
            endpoint = ((hopsize * hop) + self.min_samples - 1))
            if endpoint > len(segment):
                endpoint = len(segment)-1
            current_segment = self.raw[hop*hopsize:endpoint]
            current_rms = self.get_rms(current_segment)
            result = self.check_segment(level+1, np.square(current_segment), current_rms)
            if result == False:
                if endpoint-start_point-self.min_samples >= min_samples:
                    self.add_to_silence_labels(start_point, endpoint(previous one...))
                    start_point = endpoint
                else:
                    start_point = endpoint

        finally: if still going, make this a label, too...


    def check_segment(self, level, segment, reference_rms):
        current_rms = self.get_rms(segment)
        if ((current_rms / reference_rms) < rms_ratios[level]):
            if level < self.max_level:
                subsegment_length = int(segment * self.subsegment_percentages[level])
                hopsize = int(subsegment_length * self.hopsize_percentages[level])
                num_hops = ((len(segment) - subsegment_length)/hopsize) + 1
                for hop in range(num_hops):
                    endpoint = ((hopsize * hop) + subsegment_length - 1))
                    if endpoint > len(segment):
                        endpoint = len(segment)-1
                    if (self.check_segment(level+1, segment[(hopsize*hop):endpoint], current_rms)) == False:
                        return False
                return True
            else:
                return True
        else:
            return False


    def get_rms(self, segment):
        return np.sqrt(np.mean(segment))


    def generate_silence_labels(self):

        self.in_loop = False
        start_point = None
        end_point = None

        current_segment = self.raw[0:self.window_width]
        current_seg_square = np.square(current_segment)

        for hop in range(int((self.rawlen - self.window_width) / self.hop_size)):

            RMS = self.get_rms(current_seg_square)

            if (RMS < self.rms_threshold) & (np.amax(current_seg_square) < self.maxamp):
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
                self.silence_labels.append([start_point, end_point])

        return(self.silence_labels)

    def export_text_file(self):
        textfile = open(self.filename[:-4] + "_Labels.txt", "w")
        for entry in self.silence_labels:
            textfile.write(str(entry[0]/float(44100)) + "\t" + str(entry[1]/float(44100)) + "\n")
        textfile.close()

if __name__== '__main__':
    myvar = Sdtk_Silencer("SilenceTenMono.wav")
    myvar.generate_silence_labels()
    myvar.export_text_file()
