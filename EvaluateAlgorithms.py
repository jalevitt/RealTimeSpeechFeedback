# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 09:22:30 2020

@author: jalevitt
"""

import numpy as np
import scipy as sp
import FormantFinder
import yin
import wave
import csv
import matplotlib.pyplot as plt

CHUNK_SIZE = 8192

def ReadAudioFile(path):
    audioFile = wave.openfp(path, 'rb')
    fs = audioFile.getframerate() #get fs
    n = audioFile.getnframes() # get length
    data = np.frombuffer(audioFile.readframes(n), dtype = np.int16) 
    return fs, data
    
def ReadFormantCSV(path):
    with open(path) as csvfile:
        csvreader = csv.reader(csvfile)
        data = np.zeros([12])
        for row in csvreader:
            #print(data.shape)
            temp1 = np.array(row)
            temp2 = np.zeros([12], dtype = np.float32)
            for i in range(12):
                try:
                    temp2[i] = np.array(temp1[i], dtype = np.float32)
                except:
                    temp2[i] = np.nan
            #print(temp.shape)
            data = np.concatenate((data, temp2), 1)
        data = np.reshape(data, (len(data)/12, 12))
        
        data = data[2:, :]
        print(data)
        print(data.shape)
        return data
        
def getLPCFormantsAtTime(Recording, fs, Time, ds_rate = 3, smooth = 1):
    Formants = np.zeros(5)
    Count = np.zeros(5)
    chunkSize = CHUNK_SIZE
    for i in range(-1 * smooth / 2 + 1, 1 + smooth / 2):
        
        idx = (np.round(Time * fs) - chunkSize / 2) - (i * chunkSize/2)
        data = Recording[idx:idx + chunkSize]
        ds_data = data[0:chunkSize:ds_rate]
        f = FormantFinder.findFormantsLPC(ds_data, fs / ds_rate)
        if len(f) >= 5:
            Formants[0:5]  += f[0:5]
            Count += 1
        else:
            Formants[0:len(f)] += f
            Count[0:len(f)] += 1
    for i in range(5):
        if Count[i] > 0:
            Formants[i] /= Count[i]
        else:
            Formants[i] = np.nan
    return Formants
    
def getAllLPCFormants(Recording, fs, PraatData, ds_rate = 3, smooth = 1):
    s = PraatData.shape
    numRows = s[0]
    LPCFormants = np.zeros((numRows, 5))
    PRAATFormants = np.zeros((numRows, 5))
    for row in range(numRows):
        t = PraatData[row, 0]
        
        Formants = getLPCFormantsAtTime(Recording, fs, t, ds_rate, smooth)
        if len(Formants) >= 5:
            LPCFormants[row, 0:5] = Formants[0:5]
            for i in range(len(Formants), 5):
                LPCFormants[row, i] = np.nan
        else:
            LPCFormants[row, 0:len(Formants)] = Formants
        PRAATFormants[row, :] = PraatData[row, 2:12:2]
            
    return LPCFormants, PRAATFormants
    
def compareLPCPRAAT(LPCFormants, PRAATFormants, fi, robust = True):
    LPC = LPCFormants[:, fi - 1]
    for i in range(len(LPC)):
        if LPC[i] == 0:
            LPC[i] = np.nan
            
    PRAAT = PRAATFormants[:, fi - 1]
    LPCNan = np.isnan(LPC)
    PRAATNan = np.isnan(PRAAT)
    LPC = LPC[~LPCNan & ~PRAATNan]
    PRAAT = PRAAT[~LPCNan & ~PRAATNan]
    
    slope, intercept, r, p, stdErr = sp.stats.linregress(PRAAT, LPC)
    roSlope, roIntercept, a, b = sp.stats.mstats.theilslopes(LPC, x = PRAAT)
    x = np.linspace(0, 5500, 10)
    y = x * slope + intercept
    y_robust = x * roSlope + roIntercept
    LPCPredict = PRAAT * roSlope + roIntercept
    stat = sp.stats.pearsonr(LPC, LPCPredict)
    p_robust = stat[1]
    MAE = np.mean(np.abs(PRAAT - LPC))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)    
    ax = plt.axes()
    ax.scatter(PRAAT, LPC)
    if robust:
    
        ax.plot(x, y_robust, color = 'red')
        strData = 'Slope = ' + str(roSlope) + '\nIntercept = ' + str(roIntercept) + '\nMAE = ' + str(MAE) + '\nP = ' + str(p_robust)
    else:
        ax.plot(x, y)
        strData = 'Slope = ' + str(roSlope) + '\nIntercept = ' + str(roIntercept) + '\nR-Squared = ' + str(r**2) + '\nP = ' + str(p)

    ax.text(0.6, 0.2, strData, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    ax.set_xlabel('PRAAT Formant')
    ax.set_ylabel('LPC Formant')
    ax.set_xlim((0, 5500))
    ax.set_ylim((0, 5500))
    ax.set_title('Formant ' + str(fi))
    plt.show()

def ReadPitchCSV(path):
    with open(path) as pitchFile:
        csvReader = csv.reader(pitchFile, delimiter = '\t')
        next(csvReader)
        data = np.zeros([2], dtype = np.float32)
        for row in csvReader:
            data = np.concatenate((data, np.array(row[1:], dtype = np.float32)), 1)
            
        data = np.reshape(data, (len(data)/2, 2))
        data = data[1:, :]
        print(data)
        print(data.shape)
        return data

def getYinPitchAtTime(Recording, fs, Time):
    chunkSize = CHUNK_SIZE
    idx = np.round(Time * fs) - chunkSize / 2
    data = Recording[idx:idx + chunkSize]
    data = data * np.hamming(chunkSize)
    df = yin.differenceFunction(data, chunkSize, fs/75)
    cmndf = yin.cumulativeMeanNormalizedDifferenceFunction(df, len(df))
    f0 = yin.getPitch(cmndf, fs/500, fs/75, harmo_th = 0.35)
    return f0    
    
def getAllYinPitch(Recording, fs, PraatData):
    s = PraatData.shape
    numRows = s[0]
    YinPitch = np.zeros((numRows, 1))
    PRAATPitch = np.zeros((numRows, 1))
    for row in range(numRows):
        t = PraatData[row, 0]
        f0 = getYinPitchAtTime(Recording, fs, t)
        if f0:
            YinPitch[row] = 1.0 * fs / f0
        else:
            YinPitch[row] = np.nan
        PRAATPitch[row] = PraatData[row, 1]
        
    return YinPitch, PRAATPitch
    
def compareYinPRAAT(YinPitch, PRAATPitch, robust = True):
    Yin = YinPitch
    for i in range(len(Yin)):
        if Yin[i] == 0:
            Yin[i] = np.nan
            
    PRAAT = PRAATPitch
    YinNan = np.isnan(Yin)
    PRAATNan = np.isnan(PRAAT)
    Yin = Yin[~YinNan & ~PRAATNan]
    PRAAT = PRAAT[~YinNan & ~PRAATNan]
    print(Yin.shape)
    slope, intercept, r, p, stdErr = sp.stats.linregress(PRAAT, Yin)
    roSlope, roIntercept, a, b = sp.stats.mstats.theilslopes(Yin, x = PRAAT)
    x = np.linspace(0, 500, 10)
    y = x * slope + intercept
    y_robust = x * roSlope + roIntercept
    YinPredict = PRAAT * roSlope + roIntercept
    stat = sp.stats.pearsonr(Yin, YinPredict)
    p_robust = stat[1]
    MAE = np.mean(np.abs(PRAAT - Yin))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)    
    ax = plt.axes()
    ax.scatter(PRAAT, Yin)
    if robust:
    
        ax.plot(x, y_robust, color = 'red')
        strData = 'Slope = ' + str(roSlope) + '\nIntercept = ' + str(roIntercept) + '\nMAE = ' + str(MAE) + '\nP = ' + str(p_robust)
    else:
        ax.plot(x, y)
        strData = 'Slope = ' + str(roSlope) + '\nIntercept = ' + str(roIntercept) + '\nR-Squared = ' + str(r**2) + '\nP = ' + str(p)

    ax.text(0.6, 0.2, strData, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    ax.set_xlabel('PRAAT Pitch')
    ax.set_ylabel('YIN Pitch')
    ax.set_xlim((0, 500))
    ax.set_ylim((0, 500))
    ax.set_title('Fundamental Frequency')
    plt.show()

FormantCSVPath = ''
WavPath = 'C:\Users\Josh Levitt\Documents\RealTimeSpeechFeedback-working\TestData\JoshTestVon.wav'
PitchCSVPath = 'C:\Users\Josh Levitt\Documents\RealTimeSpeechFeedback-working\TestData\JoshTestVonF0_PRAAT.csv'
fs, AudioData = ReadAudioFile(WavPath)
'''
PraatFormantData = ReadFormantCSV(FormantCSVPath)
LPCFormants, PRAATFormants = getAllLPCFormants(AudioData, fs, PraatFormantData, 1, 1)
compareLPCPRAAT(LPCFormants, PRAATFormants, 5, True)
'''
PraatPitchData = ReadPitchCSV(PitchCSVPath)
YinPitch, PRAATPitch = getAllYinPitch(AudioData, fs, PraatPitchData)
compareYinPRAAT(YinPitch, PRAATPitch, True)
