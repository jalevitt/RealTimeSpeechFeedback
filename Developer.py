# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:41:12 2020

@author: Josh Levitt
"""

import sys
from PyQt4 import QtCore, QtGui
import PyAudioTest
import pyaudio
import numpy as np
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from matplotlibwidget import MatplotlibWidget

import matplotlib.pyplot as plt
import wave
import time as ti
import yin # use yin toolbox found online, see file yin.py for accreditation
import scipy as sp
import FormantFinder # formant algorithm found online, see FormantFinder.py for accreditation
import csv
import warnings
import ReportMain
import DeveloperUI
import UserMain

warnings.filterwarnings("ignore")

class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = DeveloperUI.Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        # set up button callbacks  
        
        self.ui.Go.clicked.connect(self._GoRun)
        self.ui.LoadData.clicked.connect(self._Load)
        self.ui.PlayBack.clicked.connect(self._Playback)
        self.ui.Save.clicked.connect(self._SaveRecording)
        self.ui.Stop.clicked.connect(self._StopRun)
        self.ui.SaveFormants.clicked.connect(self._SaveF)
        self.ui.SavePitch.clicked.connect(self._SaveP)
        self.ui.ReportButton.clicked.connect(self._MakeReport)
        self.ui.UserMode.clicked.connect(self._LaunchUserMode)
        
        # set up some vriables
        self.ui.Recording = np.zeros(100000, dtype = np.int16)
        self.ui.Status = False
        self.ui.fs = 44100
        self.ui.Formants = np.zeros((100, 5), dtype = np.float32)
        self.ui.FormantTime = np.zeros(100, dtype = np.float32)
        self.ui.Pitch = np.zeros(100, dtype = np.float32)
        self.ui.PitchTime = np.zeros(100, dtype = np.float32)
        self.ui.Time = np.zeros(1000, dtype = np.float32)
        self.ui.Targets = np.zeros((1000, 3), dtype = np.float32)
        
        # set up axes labels etc        
        ax = self.ui.RawPlot.figure.add_subplot(111)
        ax.set_title('Raw Waveform')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        PSDax = self.ui.PSDPlot.figure.add_subplot(111)
        PSDax.set_title('Power Spectrum')
        PSDax.set_xlabel('Frequency (Hz)')
        PSDax.set_ylabel('Power')
        f0ax = self.ui.FundamentalFrequenncyPlot.figure.add_subplot(111)
        f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        f0ax.set_position([0.35, 0.05, 0.6, 0.93])
        f0ax.set_ylabel('Fundamental Frequency (Hz)')
        f0ax.set_ylim((0, 500))
        f0ax.set_xlim((0, 0.8))

        tractAx = self.ui.VocalTractPlot.figure.add_subplot(111)
        tractAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        tractAx.set_position([0.35, 0.05, 0.6, 0.93])
        tractAx.set_ylabel('Vocal Tract Length (cm)')
        tractAx.set_ylim((0, 25))
        tractAx.set_xlim((0, 0.8))
        
        VarAx = self.ui.PitchVar.figure.add_subplot(111)
        VarAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        VarAx.set_position([0.35, 0.05, 0.6, 0.93])
        VarAx.set_ylabel('Pitch Variability (Semitones)')
        VarAx.set_ylim((0, 25))
        VarAx.set_xlim((0, 0.8))
        
    def _LaunchUserMode(self):
        UserMain.Main(parent = self).show()
        
    def _MakeReport(self):
        print('Generating Report...')
        ReportMain.ReportWindow(self).show()
        
        
        
    def _StopRun(self):
        #stop recording/playback
        self.ui.Status = False
        
    def _SaveF(self): 
        # save formants
        root = Tk()
        path = tkFileDialog.asksaveasfilename() #choose file name
        if not path:
            print('Invalid filename')
            root.destroy()
            return False
        #write to csv    
        with open(path, 'w') as csvfile:
            FormantWriter = csv.writer(csvfile, delimiter = ',', lineterminator ='\n')
            FormantWriter.writerow(['time(s)', 'f1 (Hz)', 'f2 (Hz)', 'f3 (Hz)', 'f4 (Hz)', 'f5 (Hz)'])
            for i in range(len(self.ui.FormantTime)):
                FormantWriter.writerow(np.concatenate((self.ui.FormantTime[i], self.ui.Formants[i, :]), axis = None))
        #close stuff    
        print('Formant CSV save successful')
        root.destroy()
        return True
        
    def _SaveP(self):
        #save Pitch
        root = Tk()
        path = tkFileDialog.asksaveasfilename() #choose file to save to
        if not path:
            print('Invalid filename')
            root.destroy()
            return False
        #write to csv    
        with open(path, 'w') as csvfile:
            PitchWriter = csv.writer(csvfile, delimiter = ',', lineterminator ='\n')
            PitchWriter.writerow(['time(s)', 'Pitch (Hz)'])
            for i in range(len(self.ui.PitchTime)):
                PitchWriter.writerow(np.concatenate((self.ui.PitchTime[i], self.ui.Pitch[i]), axis = None))
        #close stuff      
        print('Pitch CSV save successful')
        root.destroy()
        return True
        
    def _GoRun(self): #main button callback for collecting new data
        self.ui.Status = True
        self.ui.fs = 44100 #set sample rate, default to 44100
        iters = 1000 # (mostly) deprecated
        chunkSize = 8192 #number of samples to read in at once
        numSamples = iters * chunkSize # sets an initial size for our recording buffer
        windowSize = 5
        
        #set up an audio stream
        p = pyaudio.PyAudio()
        audioStream = p.open(format = pyaudio.paInt16, channels = 1, rate = self.ui.fs, 
                             input = True, frames_per_buffer = chunkSize)
                             
        #empty out the recording
        self.ui.Recording = np.zeros(numSamples, dtype = np.int16)
        self.ui.Formants = np.zeros((100, 5), dtype = np.float32)
        self.ui.FormantTime = np.zeros(100, dtype = np.float32)
        self.ui.Pitch = np.zeros(100, dtype = np.float32)
        self.ui.PitchTime = np.zeros(100, dtype = np.float32)
        FormantCount = 0
        PitchCount = 0
        
        #set up our axes
        ax = self.ui.RawPlot.figure.add_subplot(111)
        ax.set_title('Raw Waveform')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        PSDax = self.ui.PSDPlot.figure.add_subplot(111)
        PSDax.set_title('Power Spectrum')
        PSDax.set_xlabel('Frequency (Hz)')
        PSDax.set_ylabel('Power')                
        f0ax = self.ui.FundamentalFrequenncyPlot.figure.add_subplot(111)
        f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        f0ax.set_position([0.35, 0.05, 0.6, 0.93])        
        tractAx = self.ui.VocalTractPlot.figure.add_subplot(111)
        tractAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        tractAx.set_position([0.35, 0.05, 0.6, 0.93])
        tractAx.set_ylabel('Vocal Tract Length (cm)')
        tractAx.set_ylim((0, 25))
        tractAx.set_xlim((0, 0.8))
        VarAx = self.ui.PitchVar.figure.add_subplot(111)
        VarAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        VarAx.set_position([0.35, 0.05, 0.6, 0.93])
        VarAx.set_ylabel('Pitch Variability (Semitones)')
        VarAx.set_ylim((0, 25))
        VarAx.set_xlim((0, 0.8))
        
        c = 34300 # speed of sound in cm/s
        maxPitchLag = 3 #winodw size for calculating pitch in sec
        maxVocalLag = 3 #winodw size for calculating VTL in sec
        maxPitchVarLag = 10 #window size for calculating pitch var in sec
        
        #initialize vars
        meanPitch = 0
        meanTractLength = 0
        stdPitch = 0
        STVarPitch = 0
        
        time = np.linspace(0, numSamples / self.ui.fs, numSamples)
        ds_rate = 3
        #set up time vector
        print('Beginning New Recording')
        i = 0
        try: #using try/except to enable keyboard interrupt
            start = ti.time()
            while self.ui.Status:  #keep going forever, or until keyboard interrupt
                t = (i  + 1) * chunkSize     
                
                if t > len(self.ui.Recording): # add space to the recording in necessary
                    extraSpace = np.zeros(numSamples, dtype = np.int16)
                    self.ui.Recording = np.concatenate([self.ui.Recording, extraSpace], axis = None)
                    time = np.linspace(0, len(self.ui.Recording) / self.ui.fs, len(self.ui.Recording))
                    
                # pull a chunk from our audio stream
                data = PyAudioTest.getChunk(chunkSize, audioStream, Random = 0)   
                data_ds = data[0:chunkSize:ds_rate] # downsample of data
                # its generally a good idea to lowpass filter before downsampling, 
                # but to save computational time this is skipped here.
                # our data is ~mostly~ band-limited, so I don't expect this to be huge problem
                
                # add chunk to our recording
                self.ui.Recording[i * chunkSize:(i + 1) * chunkSize] = data
                
                # get f0 and update f0 plot                
                # use yin implementation instead
                # yin's original implementation called for filtering, 
                # which we have not yet implemented for computational reasons
                data_hamming = data * np.hamming(chunkSize)
                df = yin.differenceFunction(data_hamming, chunkSize, self.ui.fs/75)
                cmndf = yin.cumulativeMeanNormalizedDifferenceFunction(df, len(df))
                f0 = yin.getPitch(cmndf, self.ui.fs/500, self.ui.fs/75, harmo_th = 0.35)
                
                if f0: # if f0 is detected, update our graph
                    # store ot pitch and time
                    self.ui.Pitch[PitchCount] = 1.0 * self.ui.fs/f0
                    self.ui.PitchTime[PitchCount] = 1.0 * (t - chunkSize / 2) / self.ui.fs
                    PitchCount += 1
                    # add space if needed
                    if PitchCount >= len(self.ui.PitchTime):
                        self.ui.Pitch = np.concatenate((self.ui.Pitch, np.zeros(200, dtype = np.float32)))
                        self.ui.PitchTime = np.concatenate((self.ui.PitchTime, np.zeros(200, dtype = np.float32)))
                        
                    #get pitches from the last 3 seconds
                    RecentPitches = []
                    pitchIDX = PitchCount - 1
                    while self.ui.PitchTime[pitchIDX] >= 1.0 * (t - chunkSize / 2) / self.ui.fs - maxPitchLag and pitchIDX >= 0:
                        RecentPitches.append(self.ui.Pitch[pitchIDX])
                        pitchIDX -= 1
                        
                    meanPitch = np.mean(RecentPitches)
                    h = 2.0
                    f0ax.clear()
                    f0ax.hold(True)
                    f0ax.bar([0], [2.0 * h], bottom = [meanPitch - h])
                    f0ax.bar([0], [2.0 * h], bottom = [self.ui.PitchTarget.value() - h], color = 'black')
                    f0ax.set_ylabel('Fundamental Frequency (Hz)')
                    f0ax.set_ylim((0, 500))
                    f0ax.set_xlim((0, 0.8))
                    self.ui.FundamentalFrequenncyPlot.draw()
                                        
                    RecentPitches = []
                    pitchIDX = PitchCount - 1
                    while self.ui.PitchTime[pitchIDX] >= 1.0 * (t - chunkSize / 2) / self.ui.fs - maxPitchVarLag and pitchIDX >= 0:
                        RecentPitches.append(self.ui.Pitch[pitchIDX])
                        pitchIDX -= 1
                        
                    if len(RecentPitches) > 1:
                        stdPitch = np.std(RecentPitches)
                        meanPitch = np.mean(RecentPitches)
                    else:
                        stdPitch = 0
                    
                    #convert to semitones
                    RPitch = np.array(RecentPitches)
                    RPitch = 39.86 * np.log10(RPitch / meanPitch)
                    
                    if len(RPitch) > 1:
                        STVarPitch = np.std(RPitch)
                        
                    else:
                        STVarPitch = 0
                    
                    # make pitch variability bar graph
                    h = 0.1
                    VarAx.clear()
                    VarAx.hold(True)
                    VarAx.bar([0], [2.0 * h], bottom = [STVarPitch - h])
                    VarAx.bar([0], [2.0 * h], bottom = [self.ui.VarTarget.value() - h], color = 'black')
                    VarAx.set_ylabel('Pitch Variability (Semitones)')
                    VarAx.set_ylim((0, 25))
                    VarAx.set_xlim((0.0, 0.8))
                    self.ui.PitchVar.draw()
                    
                
                PSDax.clear()
                PSDax.hold(True)
                if f0:
                    try:
                        fBins, PSD = sp.signal.periodogram(data_ds, self.ui.fs / ds_rate)
                        PSD = 20 * np.log10(PSD)
                        Formants = FormantFinder.findFormantsLPC(data_ds, self.ui.fs / ds_rate)
                        
                        for f in range(len(Formants)): # plot the formants as  vertical lines
                            PSDax.plot([Formants[f], Formants[f]], [-100, 75], color = 'red')
                            
                            
                        PSDax.plot(fBins, PSD)
                        PSDax.set_title('Power Spectrum - Formants')
                        PSDax.set_xlabel('Frequency (Hz)')
                        PSDax.set_ylabel('Power (dB)')
                        PSDax.set_ylim((-90, 90))
                        PSDax.set_xlim((0, 5000))
                        self.ui.PSDPlot.draw()
                        PSDax.hold(False)

                        
                        #store Formants
                        if len(Formants) >= 5:
                            self.ui.Formants[FormantCount, 0:5] = Formants[0:5]
                        else:
                            self.ui.Formants[FormantCount, 0:len(Formants)] = Formants
                        self.ui.FormantTime[FormantCount] = 1.0 * (t - chunkSize / 2) / self.ui.fs
                        FormantCount += 1
                        # add space if needed
                        if FormantCount >= len(self.ui.FormantTime):
                            self.ui.Formants = np.concatenate((self.ui.Formants, np.zeros((200, 5), dtype = np.float32)))
                            self.ui.FormantTime = np.concatenate((self.ui.FormantTime, np.zeros(200, dtype = np.float32)))
                        
                        #detect recent vocal tract lengths
                        RecentTractLength = []
                        tractIDX = FormantCount - 1
                        while self.ui.FormantTime[tractIDX] >= 1.0 * (t - chunkSize / 2) / self.ui.fs - maxVocalLag and tractIDX >= 0:
                            vtl = FormantFinder.getVocalTractLength(self.ui.Formants[tractIDX, :], c, method = 'lammert')
                            if vtl > 9 and vtl < 25: 
                                RecentTractLength.append(vtl)
                            tractIDX -= 1
                            
                        meanTractLength = np.median(RecentTractLength)
                        h = 0.1
                        tractAx.clear()
                        tractAx.hold(True)
                        tractAx.bar([0], [2 * h], bottom = [meanTractLength - h])
                        tractAx.bar([0], [2 * h], bottom = [self.ui.VTLTarget.value() - h], color = 'black')
                        
                        tractAx.set_ylabel('Vocal Tract Length (cm)')
                        tractAx.set_ylim((0, 25))
                        tractAx.set_xlim((0, 0.8))
                        self.ui.VocalTractPlot.draw()
                            
                    except (RuntimeError): #formant detection can throw errors sometimes
                        Formants = np.zeros(3)
                
                
                #update our raw data plot, but only everyother chunk, because its time consuming
                if t > windowSize * self.ui.fs and i % 3 == 0:
                    ax.plot(time[t - windowSize * self.ui.fs:t], 
                            self.ui.Recording[t - windowSize * self.ui.fs:t])
                    ax.set_title('Raw Waveform')
                    ax.set_xlabel('Time (s)')
                    ax.set_ylabel('amplitude')
                    self.ui.RawPlot.draw()
                    
                    
                #keep track of our target values, in case they chane over time
                if i >= len(self.ui.Time): # add extra space to vectors in case we need it
                    self.ui.Time = np.concatenate((self.ui.Time,  np.zeros(1000, dtype = np.float32)))
                    self.ui.Targets = np.concatenate((self.ui.Targets, np.zeros((1000, 3), dtype = np.float32)))
                    
                self.ui.Time[i] = 1.0 * t / self.ui.fs
                self.ui.Targets[i, 0] = self.ui.PitchTarget.value() 
                self.ui.Targets[i, 1] = self.ui.VTLTarget.value()
                self.ui.Targets[i, 2] =self.ui.VarTarget.value()
                i += 1
                
                #check for incoming button clicks i.e. stop button
                QtCore.QCoreApplication.processEvents()

        except (KeyboardInterrupt, SystemExit): # in case of a keyboard interrupt or system exit, clean house
            
            self.ui.RawPlot.draw()
            self.ui.FundamentalFrequenncyPlot.draw()
            #truncate zero pads
            self.ui.Pitch = self.ui.Pitch[0:PitchCount]
            self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
            self.ui.Formants = self.ui.Formants[0:FormantCount, :]
            self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]
            self.ui.Time = self.ui.Time[0:i]
            self.ui.Targets = self.ui.Targets[0:i, :]
            print('Recording Completed')
            self.ui.Recording = self.ui.Recording[0:t]
            print('recorded time is')
            print(1.0 * t / self.ui.fs)
            print('elapsed time is:')
            print(ti.time() - start)
            return True            
        #truncate zero pads
        self.ui.Pitch = self.ui.Pitch[0:PitchCount]
        self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
        self.ui.Formants = self.ui.Formants[0:FormantCount, :]
        self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]
        self.ui.Time = self.ui.Time[0:i]
        self.ui.Targets = self.ui.Targets[0:i, :]
        print('Recording Completed')
        self.ui.Recording = self.ui.Recording[0:t]
        print('recorded time is')
        print(1.0 * t / self.ui.fs)
        print('elapsed time is:')
        print(ti.time() - start)
        return True
        
    def _SaveRecording(self): 
        # open a save dialog so the user can select a file name
        root = Tk()
        path = tkFileDialog.asksaveasfilename()
        if not path:
            print('Invalid filename')
            root.destroy()            
            return False
        # set file parameters  
        wavFile = wave.open(path, 'w')
        wavFile.setnchannels(1)
        wavFile.setsampwidth(2)
        wavFile.setframerate(self.ui.fs)
        #write data to file        
        wavFile.writeframesraw(np.ndarray.tobytes(self.ui.Recording))
        #close everything
        wavFile.close()
        root.destroy()
        print('Save Successful')
        return True
            
            
    def _Load(self):
        # open file finder dialog UI
        root = Tk()
        root.filename = tkFileDialog.askopenfilename()
        if not root.filename:
            print('Invalid file')
            root.destroy()
            return False
            
        print(root.filename)
        # read the selected file
        audioFile = wave.openfp(root.filename, 'rb')
        self.ui.fs = audioFile.getframerate() #get fs
        n = audioFile.getnframes() # get length
        data = np.frombuffer(audioFile.readframes(n), dtype = np.int16) 
        self.ui.Recording = data # insert audio into our recording
        print("Recording Loaded successfully")
        root.destroy()
        return True
        
    def _Playback(self): # similar to Go, but uses data from Load instead of collecting new data
        self.ui.Status = True        
        chunkSize = 8192
        windowSize = 5
        p = pyaudio.PyAudio()
        audioStream = p.open(format = pyaudio.paInt16, channels = 1, rate = self.ui.fs, 
                             input = True, frames_per_buffer = chunkSize)
        
        numSamples = len(self.ui.Recording)
        self.ui.Formants = np.zeros((100, 5), dtype = np.float32)
        self.ui.FormantTime = np.zeros(100, dtype = np.float32)
        self.ui.Pitch = np.zeros(100, dtype = np.float32)
        self.ui.PitchTime = np.zeros(100, dtype = np.float32)
        PitchCount = 0
        FormantCount = 0
        
        ax = self.ui.RawPlot.figure.add_subplot(111)
        ax.set_title('Raw Waveform')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        PSDax = self.ui.PSDPlot.figure.add_subplot(111)
        PSDax.set_title('Power Spectrum')
        PSDax.set_xlabel('Frequency (Hz)')
        PSDax.set_ylabel('Power')
        
        f0ax = self.ui.FundamentalFrequenncyPlot.figure.add_subplot(111)
        f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        f0ax.set_position([0.35, 0.05, 0.6, 0.93])
        tractAx = self.ui.VocalTractPlot.figure.add_subplot(111)
        tractAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        tractAx.set_position([0.35, 0.05, 0.6, 0.93])
        tractAx.set_ylabel('Vocal Tract Length (cm)')
        tractAx.set_ylim((0, 25))
        tractAx.set_xlim((0, 0.8))
        VarAx = self.ui.PitchVar.figure.add_subplot(111)
        VarAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        VarAx.set_position([0.35, 0.05, 0.6, 0.93])
        VarAx.set_ylabel('Pitch Variability (Hz)')
        VarAx.set_ylim((0, 25))
        VarAx.set_xlim((0, 0.8))
        
        maxPitchLag = 3
        maxVocalLag = 3
        maxPitchVarLag = 10
        meanPitch = 0
        meanTractLength = 0
        stdPitch = 0
        STVarPitch = 0
        
        
        ds_rate = 3
        
        c = 34300 # speed of sound in cm/s
        
        time = np.linspace(0, numSamples / self.ui.fs, numSamples)
        Count = 0
        t = 0
        print('Beginning Playback')
        try:
            start = ti.time()
            while t < numSamples - chunkSize and self.ui.Status:
                t += chunkSize
                data = PyAudioTest.getChunk(chunkSize, audioStream, Random = 0)
                data = self.ui.Recording[t - chunkSize:t]
                data_ds = data[0:chunkSize:ds_rate] 
                
                # use yin implementation
                data_hamming = data * np.hamming(chunkSize)
                df = yin.differenceFunction(data_hamming, chunkSize, self.ui.fs/75)
                cmndf = yin.cumulativeMeanNormalizedDifferenceFunction(df, len(df))
                f0 = yin.getPitch(cmndf, self.ui.fs/500, self.ui.fs/75, harmo_th = 0.35)
                
                if f0:
                    # store ot pitch and time
                    self.ui.Pitch[PitchCount] = 1.0 * self.ui.fs/f0
                    self.ui.PitchTime[PitchCount] = 1.0 * (t - chunkSize / 2) / self.ui.fs
                    PitchCount += 1
                    # add space if needed
                    if PitchCount >= len(self.ui.PitchTime):
                        self.ui.Pitch = np.concatenate((self.ui.Pitch, np.zeros(200, dtype = np.float32)))
                        self.ui.PitchTime = np.concatenate((self.ui.PitchTime, np.zeros(200, dtype = np.float32)))
                    
                    RecentPitches = []
                    pitchIDX = PitchCount - 1
                    while self.ui.PitchTime[pitchIDX] >= 1.0 * (t - chunkSize / 2) / self.ui.fs - maxPitchLag and pitchIDX >= 0:
                        RecentPitches.append(self.ui.Pitch[pitchIDX])
                        pitchIDX -= 1
                        
                    meanPitch = np.mean(RecentPitches)
                    h = 2.0
                    f0ax.clear()
                    f0ax.hold(True)
                    f0ax.bar([0], [2.0 * h], bottom = [meanPitch - h])
                    f0ax.bar([0], [2.0 * h], bottom = [self.ui.PitchTarget.value() - h], color = 'black')
                    f0ax.set_ylabel('Fundamental Frequency (Hz)')
                    f0ax.set_ylim((0, 500))
                    f0ax.set_xlim((0, 0.8))
                    
                    self.ui.FundamentalFrequenncyPlot.draw()
                    
                    RecentPitches = []
                    pitchIDX = PitchCount - 1
                    while self.ui.PitchTime[pitchIDX] >= 1.0 * (t - chunkSize / 2) / self.ui.fs - maxPitchVarLag and pitchIDX >= 0:
                        RecentPitches.append(self.ui.Pitch[pitchIDX])
                        pitchIDX -= 1
                        
                    if len(RecentPitches) > 1:
                        stdPitch = np.std(RecentPitches)
                        meanPitch = np.mean(RecentPitches)
                    else:
                        stdPitch = 0
                    
                    #convert to semitones
                    RPitch = np.array(RecentPitches)
                    RPitch = 39.86 * np.log10(RPitch / meanPitch)
                    
                    if len(RPitch) > 1:
                        STVarPitch = np.std(RPitch)
                        
                    else:
                        STVarPitch = 0
                        
                    h = 0.1
                    VarAx.clear()
                    VarAx.hold(True)
                    VarAx.bar([0], [2.0 * h], bottom = [STVarPitch - h])
                    VarAx.bar([0], [2.0 * h], bottom = [self.ui.VarTarget.value() - h], color = 'black')
                    VarAx.set_ylabel('Pitch Variability (Semitones)')
                    VarAx.set_ylim((0, 25))
                    VarAx.set_xlim((0.0, 0.8))
                    self.ui.PitchVar.draw()
                    
                
                PSDax.clear()
                PSDax.hold(True)
                if f0:
                    try:
                        fBins, PSD = sp.signal.periodogram(data_ds, self.ui.fs / ds_rate)
                        PSD = 20 * np.log10(PSD)
                        Formants = FormantFinder.findFormantsLPC(data_ds, self.ui.fs / ds_rate)
                        
                        for f in range(len(Formants)): # plot the formants as  vertical lines
                            PSDax.plot([Formants[f], Formants[f]], [-100, 75], color = 'red')
                            
                            
                        PSDax.plot(fBins, PSD)
                        PSDax.set_title('Power Spectrum - Formants')
                        PSDax.set_xlabel('Frequency (Hz)')
                        PSDax.set_ylabel('Power (dB)')
                        PSDax.set_ylim((-90, 90))
                        PSDax.set_xlim((0, 5000))
                        self.ui.PSDPlot.draw()
                        PSDax.hold(False)
                        
                        if len(Formants) >= 5:
                            self.ui.Formants[FormantCount, 0:5] = Formants[0:5]
                        else:
                            self.ui.Formants[FormantCount, 0:len(Formants)] = Formants
                        self.ui.FormantTime[FormantCount] = 1.0 * (t - chunkSize / 2) / self.ui.fs
                        FormantCount += 1
                        # add space if needed
                        if FormantCount >= len(self.ui.FormantTime):
                            self.ui.Formants = np.concatenate((self.ui.Formants, np.zeros((200, 5), dtype = np.float32)))
                            self.ui.FormantTime = np.concatenate((self.ui.FormantTime, np.zeros(200, dtype = np.float32)))
                            
                        RecentTractLength = []
                        tractIDX = FormantCount - 1
                        while self.ui.FormantTime[tractIDX] >= 1.0 * (t - chunkSize / 2) / self.ui.fs - maxVocalLag and tractIDX >= 0:
                            vtl = FormantFinder.getVocalTractLength(self.ui.Formants[tractIDX, :], c, method = 'lammert')
                            if vtl > 9 and vtl < 25: 
                                RecentTractLength.append(vtl)
                            tractIDX -= 1
                            
                        meanTractLength = np.median(RecentTractLength)
                        h = 0.1
                        tractAx.clear()
                        tractAx.hold(True)
                        tractAx.bar([0], [2 * h], bottom = [meanTractLength - h])
                        tractAx.bar([0], [2 * h], bottom = [self.ui.VTLTarget.value() - h], color = 'black')
                        
                        tractAx.set_ylabel('Vocal Tract Length (cm)')
                        tractAx.set_ylim((0, 25))
                        tractAx.set_xlim((0, 0.8))
                        self.ui.VocalTractPlot.draw()
                            
                    except (RuntimeError):
                        Formants = np.zeros(3)
                           
                if t > windowSize * self.ui.fs and Count % 3 == 0:               
                    ax.plot(time[t - windowSize * self.ui.fs:t], 
                            self.ui.Recording[t - windowSize * self.ui.fs:t])
                    plt.xlim(t/self.ui.fs - windowSize, t/self.ui.fs + 1)
                    ax.set_xlabel('Time (s)')
                    ax.set_ylabel('amplitude')
                    ax.set_title('Raw Waveform')
                    self.ui.RawPlot.draw()
                
                if Count >= len(self.ui.Time):
                    self.ui.Time = np.concatenate((self.ui.Time,  np.zeros(1000, dtype = np.float32)))
                    self.ui.Targets = np.concatenate((self.ui.Targets, np.zeros((1000, 3), dtype = np.float32)))
                    
                self.ui.Time[Count] = 1.0 * t / self.ui.fs
                self.ui.Targets[Count, 0] = self.ui.PitchTarget.value() 
                self.ui.Targets[Count, 1] = self.ui.VTLTarget.value()
                self.ui.Targets[Count, 2] =self.ui.VarTarget.value()
                
                Count += 1    
                    
                QtCore.QCoreApplication.processEvents()
                    
        except (KeyboardInterrupt, SystemExit):
            self.ui.RawPlot.draw()
            self.ui.FundamentalFrequenncyPlot.draw()
            self.ui.Pitch = self.ui.Pitch[0:PitchCount]
            self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
            self.ui.Time = self.ui.Time[0:Count]
            self.ui.Targets = self.ui.Targets[0:Count, :]
            self.ui.Formants = self.ui.Formants[0:FormantCount, :]
            self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]
            print('Recording Completed')
            print('recorded time is')
            print(1.0 * t / self.ui.fs)
            print('elapsed time is:')
            print(ti.time() - start)
            return True            
            
        self.ui.Pitch = self.ui.Pitch[0:PitchCount]
        self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
        self.ui.Time = self.ui.Time[0:Count]
        self.ui.Targets = self.ui.Targets[0:Count, :]
        self.ui.Formants = self.ui.Formants[0:FormantCount, :]
        self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]        
        print('Recording Completed')
        print('recorded time is')
        print(1.0 * t / self.ui.fs)
        print('elapsed time is:')
        print(ti.time() - start)
 
def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()