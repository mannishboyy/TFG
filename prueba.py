import matplotlib.pyplot as plt
import librosa
import numpy as np
import csv
import glob
import math
import pandas as pd

def rms(fileCsv, fileAudio):
    with open(fileCsv, 'r') as file:
        fileReader = csv.reader(file)
        next(fileReader)
        for row in fileReader:
            begin = float(row[5])
            dur = float(row[6])
            x, sr = librosa.load(fileAudio, offset=begin, duration=dur)
            mediaxd=np.sum(x)
            rmsValue = math.sqrt(np.sum(pow(x,2))/len(x))
            print('lego')

fileCsv ='CsvFiles/Miniature1.csv'
fileAudio = 'ScoreSoundFile/score-armonic.wav'
rms(fileCsv, fileAudio)

#x, sr = librosa.load(filename)
#t = np.linspace(0, len(x)/sr, num=len(x))

#plt.figure(1)
#plt.plot(t, pow(x,2))
#plt.show()
