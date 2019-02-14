# Sdtk_Silencer

import numpy as np
import scipy.io.wavfile
import copy


class Sdtk_Silencer:
    """ Class for generating a text list of start points, end points and
        average RMS (root mean squar) values for portions of audio within a
        .wav file that are (relatively) quiet and smooth (that is,
        the ratio of small-scale RMS values to large-scale rms values is
        below some threshold).
    """

    def __init__(self,
                 wavefile,
                 min_samples,
                 subsegment_percentages = [.1, .1, .1],
                 rms_ratios = [.5, .5, .5],
                 hopsize_percentages = [.3, .3, .3]
                 ):

        self.filename = wavefile
        self.raw = scipy.io.wavfile.read(wavefile)[1]/float(32768)
        self.rawlen = len(self.raw)

        self.min_samples = min_samples

        self.subsegment_percentages = subsegment_percentages
        self.rms_ratios = rms_ratios
        self.hopsize_percentages = hopsize_percentages

        self.in_loop = None
        self.silence_labels = []

        if (len(self.subsegment_percentages) == len(self.hopsize_percentages) == len(self.rms_ratios)):
            self.max_level = len(self.subsegment_percentages) - 1


    def run_analysis(self):
        """ Iterate through successive min_samples-sized windows of the full
            audio file and recursively examine subsegments to ensure that
            the subsegment rms values are below some threshold defined by the
            larger segment rms value.  If so, export large segment start and end
            points, as well as rms average.
        """
        level = 0
        hopsize = int(self.min_samples * self.hopsize_percentages[level])
        num_hops = int((self.rawlen - self.min_samples) / hopsize) + 1
        start_point = 0
        rms_records = []
        end_point = None

        for hop in range(num_hops):
            print("loop " + str(hop))
            end_point = ((hopsize * hop) + self.min_samples - 1)
            if end_point >= self.min_samples:
                end_point = self.min_samples - 1
            current_segment = np.square(self.raw[hop * hopsize:end_point])
            current_rms = self.get_rms(current_segment)
            rms_records.append(current_rms)
            result = self.check_segment(level+1, np.square(current_segment), current_rms)
            minimum_met = False

            if result == False:
                if minimum_met:
                    self.silence_labels.append([start_point,
                                                (end_point - self.min_samples),
                                                np.mean(rms_records)])
                    start_point = end_point
                    minimum_met = False
                else:
                    start_point = end_point
            else:
                end_point += self.min_samples
                minimum_met = True

        if end_point < self.rawlen-1:
            end_point = self.rawlen-1
            current_segment = self.raw[start_point:end_point]
            current_rms = self.get_rms(current_segment)
            result = self.check_segment(level+1, np.square(current_segment), current_rms)
            if result:
                self.silence_labels.append([start_point,
                                           (end_point - self.min_samples),
                                           np.mean(rms_records)])

        print("Finished analysis.")


    def check_segment(self, level, segment, reference_rms):
        current_rms = self.get_rms(segment)
        if ((current_rms / reference_rms) < self.rms_ratios[level]):
            if level < self.max_level:
                subsegment_length = int(len(segment) * self.subsegment_percentages[level])
                hopsize = int(subsegment_length * self.hopsize_percentages[level])
                num_hops = int((len(segment) - subsegment_length)/hopsize) + 1
                for hop in range(num_hops):
                    end_point = ((hopsize * hop) + subsegment_length - 1)
                    if end_point > len(segment):
                        end_point = len(segment)-1
                    if (self.check_segment(level+1, segment[(hopsize*hop):end_point], current_rms)) == False:
                        return False
                return True
            else:
                return True
        else:
            return False


    def get_rms(self, segment):
        return np.sqrt(np.mean(segment))


    def export_text_file(self):
        textfile = open(self.filename[:-4] + "_Labels.txt", "w")
        for entry in self.silence_labels:
            textfile.write(str(entry[0]/float(44100)) + "\t" +
                           str(entry[1]/float(44100)) + "\t" +
                           str(entry[2]))
        textfile.close()


#-------------------------------------------------------------------------------

if __name__== '__main__':
    myvar = Sdtk_Silencer("snooptest.wav", 44100, [.3, .3, .3], [1, 1, 1], [.1, .1, .1])
    myvar.run_analysis()
    myvar.export_text_file()
