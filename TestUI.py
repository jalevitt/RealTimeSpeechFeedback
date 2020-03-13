# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 10:36:31 2020

@author: jalevitt
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\SteppLab\Members\Josh_Levitt\TestUI.ui'
#
# Created: Mon Mar 09 10:34:14 2020
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

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

warnings.filterwarnings("ignore")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # set up the appearance of our ui, button names, locations etc
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1084, 901)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.RawPlot = MatplotlibWidget(self.centralwidget)
        self.RawPlot.setGeometry(QtCore.QRect(10, 10, 521, 421))
        self.RawPlot.setObjectName(_fromUtf8("RawPlot"))
        self.Go = QtGui.QPushButton(self.centralwidget)
        self.Go.setGeometry(QtCore.QRect(240, 470, 75, 23))
        self.Go.setObjectName(_fromUtf8("Go"))
        self.LoadData = QtGui.QPushButton(self.centralwidget)
        self.LoadData.setGeometry(QtCore.QRect(10, 470, 101, 23))
        self.LoadData.setObjectName(_fromUtf8("LoadData"))
        self.PlayBack = QtGui.QPushButton(self.centralwidget)
        self.PlayBack.setGeometry(QtCore.QRect(120, 470, 111, 23))
        self.PlayBack.setObjectName(_fromUtf8("PlayBack"))
        self.Save = QtGui.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(320, 470, 91, 23))
        self.Save.setObjectName(_fromUtf8("Save"))
        self.FundamentalFrequenncyPlot = MatplotlibWidget(self.centralwidget)
        self.FundamentalFrequenncyPlot.setGeometry(QtCore.QRect(540, 10, 141, 421))
        self.FundamentalFrequenncyPlot.setObjectName(_fromUtf8("FundamentalFrequenncyPlot"))
        self.FormantPlot = MatplotlibWidget(self.centralwidget)
        self.FormantPlot.setGeometry(QtCore.QRect(540, 440, 521, 421))
        self.FormantPlot.setObjectName(_fromUtf8("FormantPlot"))
        self.Stop = QtGui.QPushButton(self.centralwidget)
        self.Stop.setGeometry(QtCore.QRect(240, 500, 75, 23))
        self.Stop.setObjectName(_fromUtf8("Stop"))
        self.SaveFormants = QtGui.QPushButton(self.centralwidget)
        self.SaveFormants.setGeometry(QtCore.QRect(320, 500, 91, 23))
        self.SaveFormants.setObjectName(_fromUtf8("SaveFormants"))
        self.SavePitch = QtGui.QPushButton(self.centralwidget)
        self.SavePitch.setGeometry(QtCore.QRect(320, 530, 91, 23))
        self.SavePitch.setObjectName(_fromUtf8("SavePitch"))
        self.VocalTractPlot = MatplotlibWidget(self.centralwidget)
        self.VocalTractPlot.setGeometry(QtCore.QRect(690, 10, 141, 421))
        self.VocalTractPlot.setObjectName(_fromUtf8("VocalTractPlot"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1084, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.myCallback = QtGui.QAction(MainWindow)
        self.myCallback.setObjectName(_fromUtf8("myCallback"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        # set up button callbacks         
        self.Go.clicked.connect(self.GoRun)
        self.LoadData.clicked.connect(self.Load)
        self.PlayBack.clicked.connect(self.Playback)
        self.Save.clicked.connect(self.SaveRecording)
        self.Stop.clicked.connect(self.StopRun)
        self.SaveFormants.clicked.connect(self.SaveF)
        self.SavePitch.clicked.connect(self.SaveP)
        
        # set up some vriables
        self.Recording = np.zeros(100000, dtype = np.int16)
        self.Status = False
        self.fs = 44100
        self.Formants = np.zeros((100, 5), dtype = np.float32)
        self.FormantTime = np.zeros(100, dtype = np.float32)
        self.Pitch = np.zeros(100, dtype = np.float32)
        self.PitchTime = np.zeros(100, dtype = np.float32)
        
        # set up axes labels etc        
        ax = self.RawPlot.figure.add_subplot(111)
        ax.set_title('Raw Waveform')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('amplitude')
        f0ax = self.FundamentalFrequenncyPlot.figure.add_subplot(111)
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
        formantAx = self.FormantPlot.figure.add_subplot(111)
        formantAx.set_title('Power Spectrum - Formants')
        formantAx.set_xlabel('Frequency (Hz)')
        formantAx.set_ylabel('Power (dB)')
        formantAx.set_ylim((-100, 75))
        formantAx.set_xlim((0, 5000))
        tractAx = self.VocalTractPlot.figure.add_subplot(111)
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

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Go.setText(_translate("MainWindow", "Go", None))
        self.LoadData.setText(_translate("MainWindow", "Load Existing Data", None))
        self.PlayBack.setText(_translate("MainWindow", "Playback Recording", None))
        self.Save.setText(_translate("MainWindow", "Save .wav", None))
        self.Stop.setText(_translate("MainWindow", "Stop", None))
        self.SaveFormants.setText(_translate("MainWindow", "Save Formants", None))
        self.SavePitch.setText(_translate("MainWindow", "Save Pitch", None))
        self.myCallback.setText(_translate("MainWindow", "Test", None))
        
    def StopRun(self):
        self.Status = False
        
    def SaveF(self):
        root = Tk()
        path = tkFileDialog.asksaveasfilename()
        if not path:
            print('Invalid filename')
            root.destroy()
            return False
            
        with open(path, 'w') as csvfile:
            FormantWriter = csv.writer(csvfile, delimiter = ',', lineterminator ='\n')
            FormantWriter.writerow(['time(s)', 'f1 (Hz)', 'f2 (Hz)', 'f3 (Hz)', 'f4 (Hz)', 'f5 (Hz)'])
            for i in range(len(self.FormantTime)):
                FormantWriter.writerow(np.concatenate((self.FormantTime[i], self.Formants[i, :]), axis = None))
            
        print('Formant CSV save successful')
        root.destroy()
        return True
        
    def SaveP(self):
        root = Tk()
        path = tkFileDialog.asksaveasfilename()
        if not path:
            print('Invalid filename')
            root.destroy()
            return False
            
        with open(path, 'w') as csvfile:
            PitchWriter = csv.writer(csvfile, delimiter = ',', lineterminator ='\n')
            PitchWriter.writerow(['time(s)', 'Pitch (Hz)'])
            for i in range(len(self.PitchTime)):
                PitchWriter.writerow(np.concatenate((self.PitchTime[i], self.Pitch[i]), axis = None))
            
        print('Pitch CSV save successful')
        root.destroy()
        return True
        
    def GoRun(self): #main button callback for collecting new data
        self.Status = True
        self.fs = 44100 #set sample rate, default to 44100
        iters = 1000 # (mostly) deprecated
        chunkSize = 8192 #number of samples to read in at once
        windowSize = 3 #number of seconds to plot at once
        numSamples = iters * chunkSize
        
        #set up an audio stream
        p = pyaudio.PyAudio()
        audioStream = p.open(format = pyaudio.paInt16, channels = 1, rate = self.fs, 
                             input = True, frames_per_buffer = chunkSize)
                             
        #empty out the recording
        self.Recording = np.zeros(numSamples, dtype = np.int16)
        self.Formants = np.zeros((100, 5), dtype = np.float32)
        self.FormantTime = np.zeros(100, dtype = np.float32)
        self.Pitch = np.zeros(100, dtype = np.float32)
        self.PitchTime = np.zeros(100, dtype = np.float32)
        FormantCount = 0
        PitchCount = 0
        
        #set up our axes
        ax = self.RawPlot.figure.add_subplot(111)                
        f0ax = self.FundamentalFrequenncyPlot.figure.add_subplot(111)
        f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        f0ax.set_position([0.35, 0.05, 0.6, 0.93])        
        formantAx = self.FormantPlot.figure.add_subplot(111)
        tractAx = self.VocalTractPlot.figure.add_subplot(111)
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
        
        c = 34300 # speed of sound in cm/s
        maxPitchLag = 3
        ds_rate = 3
        #set up time vector
        print('Beginning New Recording')
        time = np.linspace(0, numSamples / self.fs, numSamples)
        i = 0
        try: #using try/except to enable keyboard interrupt
            start = ti.time()
            while self.Status:  #keep going forever, or until keyboard interrupt
                t = (i  + 1) * chunkSize     
                
                if t > len(self.Recording): # add space to the recording in necessary
                    extraSpace = np.zeros(numSamples, dtype = np.int16)
                    self.Recording = np.concatenate([self.Recording, extraSpace], axis = None)
                    time = np.linspace(0, len(self.Recording) / self.fs, len(self.Recording))
                    
                # pull a chunk from our audio stream
                data = PyAudioTest.getChunk(chunkSize, audioStream, Random = 0)   
                data_ds = data[0:chunkSize:ds_rate] # downsample of data
                # its generally a good idea to lowpass filter before downsampling, 
                # but to save computational time this is skipped here.
                # our data is ~mostly~ band-limited, so I don't expect this to be huge problem
                
                # add chunk to our recording
                self.Recording[i * chunkSize:(i + 1) * chunkSize] = data
                
                # get f0 and update f0 plot
                # use my hack method for getting f0
                #clipData = PyAudioTest.centerClip(data)
                #acf = PyAudioTest.autocorr(clipData)
                #f0 = PyAudioTest.getF0(acf, self.fs) 
                
                # use yin implementation instead
                # yin's original implementation called for filtering, 
                # which we have not yet implemented for computational reasons
                data_hamming = data * np.hamming(chunkSize)
                df = yin.differenceFunction(data_hamming, chunkSize, self.fs/75)
                cmndf = yin.cumulativeMeanNormalizedDifferenceFunction(df, len(df))
                f0 = yin.getPitch(cmndf, self.fs/500, self.fs/75, harmo_th = 0.35)
                
                if f0: # if f0 is detected, update our graph
                    # store ot pitch and time
                    self.Pitch[PitchCount] = 1.0 * self.fs/f0
                    self.PitchTime[PitchCount] = 1.0 * (t - chunkSize / 2) / self.fs
                    PitchCount += 1
                    # add space if needed
                    if PitchCount >= len(self.PitchTime):
                        self.Pitch = np.concatenate((self.Pitch, np.zeros(200, dtype = np.float32)))
                        self.PitchTime = np.concatenate((self.PitchTime, np.zeros(200, dtype = np.float32)))
                        

                    RecentPitches = []
                    pitchIDX = PitchCount - 1
                    while self.PitchTime[pitchIDX] >= 1.0 * (t - chunkSize / 2) / self.fs - maxPitchLag and pitchIDX >= 0:
                        RecentPitches.append(self.Pitch[pitchIDX])
                        pitchIDX -= 1
                    meanPitch = np.mean(RecentPitches)
                    stdPitch = np.std(RecentPitches)
                    f0ax.bar([0], [2.0 * stdPitch], bottom = [meanPitch - stdPitch])
                    f0ax.set_ylabel('Fundamental Frequency (Hz)')
                    f0ax.set_ylim((0, 500))
                    f0ax.set_xlim((0, 0.8))
                    self.FundamentalFrequenncyPlot.draw()
                    
                
                formantAx.clear()
                formantAx.hold(True)
                if f0: # if f0 is detected search for formants
                    #make PSD
                    fBins, PSD = sp.signal.periodogram(data_ds, self.fs / ds_rate)
                    PSD = 20 * np.log10(PSD) #convert to dB
                    try:
                        Formants = FormantFinder.findFormantsLPC(data_ds, self.fs / ds_rate) # look for formants using LPC method
                        for f in range(len(Formants)): # plot the formants as  vertical lines
                            formantAx.plot([Formants[f], Formants[f]], [-100, 75], color = 'red')
                            
                            
                        formantAx.plot(fBins, PSD)
                        formantAx.set_title('Power Spectrum - Formants')
                        formantAx.set_xlabel('Frequency (Hz)')
                        formantAx.set_ylabel('Power (dB)')
                        formantAx.set_ylim((-90, 90))
                        formantAx.set_xlim((0, 5000))
                        '''
                        formantAx.bar(range(len(Formants)), Formants)
                        formantAx.set_xlabel('Formant number')
                        formantAx.set_ylabel('Frequency (Hz)')
                        formantAx.set_title('Formants Frequencies')
                        formantAx.set_xlim((0, 4.8))
                        formantAx.set_ylim((0, 5000))
                        formantAx.set_xticks([0.4, 1.4, 2.4, 3.4, 4.4])
                        formantAx.set_xticklabels(['F1', 'F2', 'F3', 'F4', 'F5'])
                        '''
                        self.FormantPlot.draw()
                        formantAx.hold(False)
                        
                        #store Formants
                        if len(Formants) >= 5:
                            self.Formants[FormantCount, 0:5] = Formants[0:5]
                        else:
                            self.Formants[FormantCount, 0:len(Formants)] = Formants
                        self.FormantTime[FormantCount] = 1.0 * (t - chunkSize / 2) / self.fs
                        FormantCount += 1
                        # add space if needed
                        if FormantCount >= len(self.FormantTime):
                            self.Formants = np.concatenate((self.Formants, np.zeros((200, 5), dtype = np.float32)))
                            self.FormantTime = np.concatenate((self.FormantTime, np.zeros(200, dtype = np.float32)))
                            
                        TractLength = FormantFinder.getVocalTractLength(Formants, c)
                        tractAx.bar([0], [TractLength])
                        tractAx.set_ylabel('Vocal Tract Length (cm)')
                        tractAx.set_ylim((0, 25))
                        tractAx.set_xlim((0, 0.8))
                        self.VocalTractPlot.draw()
                            
                    except (RuntimeError): #formant detection can throw errors sometimes
                        Formants = np.zeros(3)
                        
                    
                else: # if no f0, basically do nothing
                    fBins = np.linspace(0, self.fs/2, 10)
                    PSD = np.zeros(10)
                    
                #update our raw data plot, but only everyother chunk, because its time consuming
                if t > windowSize * self.fs and i % 2 == 0:
                    ax.plot(time[t - windowSize * self.fs:t], 
                            self.Recording[t - windowSize * self.fs:t])
                    ax.set_title('Raw Waveform')
                    ax.set_xlabel('Time (s)')
                    ax.set_ylabel('amplitude')
                    self.RawPlot.draw()
                i += 1
                
                #check for incoming button clicks i.e. stop button
                QtCore.QCoreApplication.processEvents()

        except (KeyboardInterrupt, SystemExit): # in case of a keyboard interrupt or system exit, clean house
            self.FormantPlot.draw()
            self.RawPlot.draw()
            self.FundamentalFrequenncyPlot.draw()
            self.Pitch = self.Pitch[0:PitchCount]
            self.PitchTime = self.PitchTime[0:PitchCount]
            self.Formants = self.Formants[0:FormantCount, :]
            self.FormantTime = self.FormantTime[0:FormantCount]
            print('Recording Completed')
            self.Recording = self.Recording[0:t]
            print('recorded time is')
            print(1.0 * t / self.fs)
            print('elapsed time is:')
            print(ti.time() - start)
            return True            
            
        self.Pitch = self.Pitch[0:PitchCount]
        self.PitchTime = self.PitchTime[0:PitchCount]
        self.Formants = self.Formants[0:FormantCount, :]
        self.FormantTime = self.FormantTime[0:FormantCount]    
        print('Recording Completed')
        self.Recording = self.Recording[0:t]
        print('recorded time is')
        print(1.0 * t / self.fs)
        print('elapsed time is:')
        print(ti.time() - start)
        return True
        
    def SaveRecording(self): 
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
        wavFile.setframerate(self.fs)
        #write data to file        
        wavFile.writeframesraw(np.ndarray.tobytes(self.Recording))
        #close everything
        wavFile.close()
        root.destroy()
        print('Save Successful')
        return True
            
            
    def Load(self):
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
        self.fs = audioFile.getframerate() #get fs
        n = audioFile.getnframes() # get length
        data = np.frombuffer(audioFile.readframes(n), dtype = np.int16) 
        self.Recording = data # instert audio into our recording
        print(self.Recording)
        print("Recording Loaded successfully")
        root.destroy()
        return True
        
    def Playback(self): # similar to Go, but uses data from Load instead of collecting new data
        self.Status = True        
        chunkSize = 4096
        windowSize = 3
        p = pyaudio.PyAudio()
        audioStream = p.open(format = pyaudio.paInt16, channels = 1, rate = self.fs, 
                             input = True, frames_per_buffer = chunkSize)
        
        numSamples = len(self.Recording)
        self.Formants = np.zeros((100, 5), dtype = np.float32)
        self.FormantTime = np.zeros(100, dtype = np.float32)
        self.Pitch = np.zeros(100, dtype = np.float32)
        self.PitchTime = np.zeros(100, dtype = np.float32)
        PitchCount = 0
        FormantCount = 0
        
        ax = self.RawPlot.figure.add_subplot(111)
        
        
        f0ax = self.FundamentalFrequenncyPlot.figure.add_subplot(111)
        f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        f0ax.set_position([0.35, 0.05, 0.6, 0.93])
        tractAx = self.VocalTractPlot.figure.add_subplot(111)
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
        
        formantAx = self.FormantPlot.figure.add_subplot(111)
        maxPitchLag = 3
        ds_rate = 3
        
        c = 34300 # speed of sound in cm/s
        
        Count = 0
        t = 0
        print('Beginning Playback')
        time = np.linspace(0, numSamples / self.fs, numSamples)
        try:
            start = ti.time()
            while t < numSamples - chunkSize and self.Status:
                t += chunkSize
                data = PyAudioTest.getChunk(chunkSize, audioStream, Random = 0)
                data = self.Recording[t - chunkSize:t]
                data_ds = data[0:chunkSize:ds_rate] 
                # use my hack method for getting f0
                #clipData = PyAudioTest.centerClip(data)
                #acf = PyAudioTest.autocorr(clipData)
                #f0 = PyAudioTest.getF0(acf, self.fs) 
                
                # use yin implementation
                data_hamming = data * np.hamming(chunkSize)
                df = yin.differenceFunction(data_hamming, chunkSize, self.fs/75)
                cmndf = yin.cumulativeMeanNormalizedDifferenceFunction(df, len(df))
                f0 = yin.getPitch(cmndf, self.fs/500, self.fs/75, harmo_th = 0.35)
                
                if f0:
                    # store ot pitch and time
                    self.Pitch[PitchCount] = 1.0 * self.fs/f0
                    self.PitchTime[PitchCount] = 1.0 * (t - chunkSize / 2) / self.fs
                    PitchCount += 1
                    # add space if needed
                    if PitchCount >= len(self.PitchTime):
                        self.Pitch = np.concatenate((self.Pitch, np.zeros(200, dtype = np.float32)))
                        self.PitchTime = np.concatenate((self.PitchTime, np.zeros(200, dtype = np.float32)))
                    
                    RecentPitches = []
                    pitchIDX = PitchCount - 1
                    while self.PitchTime[pitchIDX] >= 1.0 * (t - chunkSize / 2) / self.fs - maxPitchLag and pitchIDX >= 0:
                        RecentPitches.append(self.Pitch[pitchIDX])
                        pitchIDX -= 1
                    meanPitch = np.mean(RecentPitches)
                    stdPitch = np.std(RecentPitches)
                    f0ax.bar([0], [2.0 * stdPitch], bottom = [meanPitch - stdPitch])
                    f0ax.set_ylabel('Fundamental Frequency (Hz)')
                    f0ax.set_ylim((0, 500))
                    f0ax.set_xlim((0, 0.8))
                    
                    self.FundamentalFrequenncyPlot.draw()
                    
                
                
                # use my terrible gaussian estimation formant finder
                formantAx.clear()
                formantAx.hold(True)
                if f0:
                    fBins, PSD = sp.signal.periodogram(data_ds, self.fs / ds_rate)
                    PSD = 20 * np.log10(PSD)
                    try:
                        Formants = FormantFinder.findFormantsLPC(data_ds, self.fs / ds_rate)
                        
                        for f in range(len(Formants)):
                            formantAx.plot([Formants[f], Formants[f]], [-100, 75], color = 'red')
                            
                            
                        formantAx.plot(fBins, PSD)
                        formantAx.set_title('Power Spectrum - Formants')
                        formantAx.set_xlabel('Frequency (Hz)')
                        formantAx.set_ylabel('Power (dB)')
                        formantAx.set_ylim((-90, 90))
                        formantAx.set_xlim((0, 5000))
                        '''
                        formantAx.bar(range(len(Formants)), Formants)
                        formantAx.set_xlabel('Formant number')
                        formantAx.set_ylabel('Frequency (Hz)')
                        formantAx.set_title('Formants Frequencies')
                        formantAx.set_xlim((0, 4.8))
                        formantAx.set_ylim((0, 5000))
                        formantAx.set_xticks([0.4, 1.4, 2.4, 3.4, 4.4])
                        formantAx.set_xticklabels(['F1', 'F2', 'F3', 'F4', 'F5'])
                        '''
                        self.FormantPlot.draw()
                        formantAx.hold(False)
                        
                        if len(Formants) >= 5:
                            self.Formants[FormantCount, 0:5] = Formants[0:5]
                        else:
                            self.Formants[FormantCount, 0:len(Formants)] = Formants
                        self.FormantTime[FormantCount] = 1.0 * (t - chunkSize / 2) / self.fs
                        FormantCount += 1
                        # add space if needed
                        if FormantCount >= len(self.FormantTime):
                            self.Formants = np.concatenate((self.Formants, np.zeros((200, 5), dtype = np.float32)))
                            self.FormantTime = np.concatenate((self.FormantTime, np.zeros(200, dtype = np.float32)))
                            
                        TractLength = FormantFinder.getVocalTractLength(Formants, c)
                        tractAx.bar([0], [TractLength])
                        tractAx.set_ylabel('Vocal Tract Length (cm)')
                        tractAx.set_ylim((0, 25))
                        tractAx.set_xlim((0, 0.8))
                        self.VocalTractPlot.draw()
                            
                    except (RuntimeError):
                        Formants = np.zeros(3)
                        
                    
                else:
                    fBins = np.linspace(0, self.fs/2, 10)
                    PSD = np.zeros(10)
                
                Count += 1    
                if t > windowSize * self.fs and Count % 4 == 0:               
                    ax.plot(time[t - windowSize * self.fs:t], 
                            self.Recording[t - windowSize * self.fs:t])
                    plt.xlim(t/self.fs - windowSize, t/self.fs + 1)
                    ax.set_xlabel('Time (s)')
                    ax.set_ylabel('amplitude')
                    ax.set_title('Raw Waveform')
                    self.RawPlot.draw()
                    
                QtCore.QCoreApplication.processEvents()
                    
        except (KeyboardInterrupt, SystemExit):
            self.FormantPlot.draw()
            self.RawPlot.draw()
            self.FundamentalFrequenncyPlot.draw()
            self.Pitch = self.Pitch[0:PitchCount]
            self.PitchTime = self.PitchTime[0:PitchCount]
            self.Formants = self.Formants[0:FormantCount, :]
            self.FormantTime = self.FormantTime[0:FormantCount]
            print('Recording Completed')
            print('recorded time is')
            print(1.0 * t / self.fs)
            print('elapsed time is:')
            print(ti.time() - start)
            return True            
            
        self.Pitch = self.Pitch[0:PitchCount]
        self.PitchTime = self.PitchTime[0:PitchCount]
        self.Formants = self.Formants[0:FormantCount, :]
        self.FormantTime = self.FormantTime[0:FormantCount]        
        print('Recording Completed')
        print('Recording Completed')
        print('recorded time is')
        print(1.0 * t / self.fs)
        print('elapsed time is:')
        print(ti.time() - start)
                



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())