import glob

import librosa
import numpy as np
import csv
import math
import pandas as pd
#COMPUTE AN ARRAY WITH THE RMS VALUES OF EACH NOTE
def rms(fileCsv, fileAudio):
   with open(fileCsv, 'r') as file:
        fileReader = csv.reader(file, dialect='excel')
        next(fileReader)
        rmsValues = ['RMS']
        for row in fileReader:
            begin = float(row[5])
            dur = float(row[6])
            x, sr = librosa.load(fileAudio, offset=begin, duration=dur)
            rmsValue = math.sqrt(np.sum(pow(x, 2)) / len(x))
            rmsValues.append(rmsValue)
        return rmsValues
#CREATES A NEW CSVFILES WITH ALL THE DATA
def reWriteCsv(readCsv, writeCsv, rmsValues):
    with open(readCsv, 'r') as reader, open(writeCsv, 'w', newline='') as writer:
        oreader = csv.reader(reader, dialect='excel')
        owriter =csv.writer(writer, dialect='excel')
        pos = 0
        for row in oreader:
            row.append(rmsValues[pos])
            owriter.writerow(row)
            pos = pos+1


all_files_nmat = glob.glob('CsvFiles/*T_nmat.csv')
all_audio_file = glob.glob('SoundFiles/*')
pos = 0
for file in all_files_nmat:
    rmsValues = rms(file, all_audio_file[pos])
    reWriteCsv(file, 'New'+file, rmsValues)
    pos = pos+1


