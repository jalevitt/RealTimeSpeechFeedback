# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:41:12 2020

@author: Josh Levitt

This file defines the behavior of the Developer mode of the UI
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
import RectSelector

warnings.filterwarnings("ignore") # warnings are for wimps.

class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # build UI
        self.ui = DeveloperUI.Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        # connect button callbacks  
        
        self.ui.Go.clicked.connect(self._GoRun)
        self.ui.LoadData.clicked.connect(self._Load)
        self.ui.PlayBack.clicked.connect(self._Playback)
        self.ui.Save.clicked.connect(self._SaveRecording)
        self.ui.Stop.clicked.connect(self._StopRun)
        self.ui.SaveFormants.clicked.connect(self._SaveF)
        self.ui.SavePitch.clicked.connect(self._SaveP)
        self.ui.ReportButton.clicked.connect(self._MakeReport)
        self.ui.UserMode.clicked.connect(self._LaunchUserMode)
        self.ui.PlotSpectrogram.clicked.connect(self._AddSpec)
        self.ui.PlotSwitch.clicked.connect(self._SwitchPlot)
        
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
        self.ui.PlotStatus = "Formants"
        
        # set up axes labels etc        
        self.ax = self.ui.RawPlot.figure.add_subplot(111)
        self.ax.set_position([0.12, 0.15, 0.82, 0.75])
        self.ax.set_title('Raw Waveform')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.PSDax = self.ui.PSDPlot.figure.add_subplot(111)
        self.PSDax.set_position([0.15, 0.15, 0.82, 0.75])
        self.PSDax.set_title('Power Spectrum')
        self.PSDax.set_xlabel('Frequency (Hz)')
        self.PSDax.set_ylabel('Power')
        self.f0ax = self.ui.FundamentalFrequenncyPlot.figure.add_subplot(111)
        self.f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.f0ax.set_position([0.35, 0.05, 0.6, 0.93])
        self.f0ax.set_ylabel('Fundamental Frequency (Hz)')
        self.f0ax.set_ylim((0, 500))
        self.f0ax.set_xlim((0, 0.8))

        self.tractAx = self.ui.VocalTractPlot.figure.add_subplot(111)
        self.tractAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.tractAx.set_position([0.35, 0.05, 0.6, 0.93])
        self.tractAx.set_ylabel('Vocal Tract Length (cm)')
        self.tractAx.set_ylim((10, 20))
        self.tractAx.set_xlim((0, 0.8))
        
        self.VarAx = self.ui.PitchVar.figure.add_subplot(111)
        self.VarAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.VarAx.set_position([0.35, 0.05, 0.6, 0.93])
        self.VarAx.set_ylabel('F0 Variability (Semitones)')
        self.VarAx.set_ylim((0, 25))
        self.VarAx.set_xlim((0, 0.8))
        
        self.FormantAx = self.ui.FormantPlot.figure.add_subplot(111)
        self.FormantAx.set_position([0.12, 0.15, 0.82, 0.75])
        self.FormantAx.set_title('Formants')
        self.FormantAx.set_ylabel('Frequency (Hz)')
        self.FormantAx.set_xlabel('Time (s)')
        self.FormantAx.set_ylim((0, 5000))
    
    # callback for switching the display from PSD (formants) to autocorrelation (F0)
    def _SwitchPlot(self):
        if self.ui.PlotStatus == "Formants":
            self.ui.PlotStatus = "F0"
        else:
            self.ui.PlotStatus = "Formants"

        print(self.ui.PlotStatus)
        return self.ui.PlotStatus
        
    # callback to add spectrogram to formants plot (only works if recording is stopped)
    def _AddSpec(self):
        if not self.ui.Status: #make sure the recording isn't running first
            FormantScatterColors = ['black', 'dimgrey', 'darkgray', 'silver', 'gainsboro', 'whitesmoke']
            self.FormantAx.clear()        # clear the axes
            self.FormantAx.hold(True)
            # make the spectrogram
            spec, f, t, im = self.FormantAx.specgram(self.ui.Recording, NFFT = 2 ** 8, 
                                                     Fs = self.ui.fs, noverlap = 2 ** 7)
            # add our formant dots
            for i in range(len(self.ui.FormantTime)):
                for f in range(5):
                    if self.ui.Formants[i, f] != 0:
                        self.FormantAx.scatter(self.ui.FormantTime[i], self.ui.Formants[i, f], color = FormantScatterColors[f])
            xmin, xmax = self.ax.get_xlim()
            self.FormantAx.set_xlim((xmin, xmax))
            self.FormantAx.set_ylim((0, 5000))
            self.FormantAx.set_title('Formants')
            self.FormantAx.set_ylabel('Frequency (Hz)')
            self.FormantAx.set_xlabel('Time (s)')
            self.ui.FormantPlot.draw()
            
    # callback to switch from developer mode to user mode 
    def _LaunchUserMode(self):
        UserMain.Main(parent = self).show()
    
    # callback to open the report window
    def _MakeReport(self):
        print('Generating Report...')
        ReportMain.ReportWindow(self).show()
        
        
    # callback to stop the recording 
    def _StopRun(self):
        #stop recording/playback
        self.ui.Status = False
        
    # callback to save formants to CSV
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
     
    # callback to save F0 to CSV
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
        
    # callback to start a recording
    def _GoRun(self): #main button callback for collecting new data
        self.ui.Status = True
        self.ui.fs = 44100 #set sample rate, default to 44100
        self.ui.Rect = None
        self.ui.Drag = None
        iters = 1000 # (mostly) deprecated
        chunkSize = 8192 #number of samples to read in at once
        numSamples = iters * chunkSize # sets an initial size for our recording buffer
        windowSize = 5 # width of our raw data plot in seconds
        
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
        self.ui.Targets = np.zeros((1000, 6), dtype = np.float32)
        FormantCount = 0
        PitchCount = 0
        
        #set up our axes
        self.ax = self.ui.RawPlot.figure.add_subplot(111)
        self.ax.set_title('Raw Waveform')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.PSDax = self.ui.PSDPlot.figure.add_subplot(111)
        self.PSDax.set_title('Power Spectrum')
        self.PSDax.set_xlabel('Frequency (Hz)')
        self.PSDax.set_ylabel('Power')                
        self.f0ax = self.ui.FundamentalFrequenncyPlot.figure.add_subplot(111)
        self.f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.f0ax.set_position([0.35, 0.05, 0.6, 0.93])        
        self.tractAx = self.ui.VocalTractPlot.figure.add_subplot(111)
        self.tractAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.tractAx.set_position([0.35, 0.05, 0.6, 0.93])
        self.tractAx.set_ylabel('Vocal Tract Length (cm)')
        self.tractAx.set_ylim((10, 20))
        self.tractAx.set_xlim((0, 0.8))
        self.VarAx = self.ui.PitchVar.figure.add_subplot(111)
        self.VarAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.VarAx.set_position([0.35, 0.05, 0.6, 0.93])
        self.VarAx.set_ylabel('Pitch Variability (Semitones)')
        self.VarAx.set_ylim((0, 25))
        self.VarAx.set_xlim((0, 0.8))
        self.FormantAx = self.ui.FormantPlot.figure.add_subplot(111)
        self.FormantAx.clear()
        self.FormantAx.set_ylabel('Frequency (Hz)')
        self.FormantAx.set_xlabel('Time (s)')
        self.FormantAx.set_ylim((0, 5000))
        self.FormantAx.hold(True)
        
        c = 34300 # speed of sound in cm/s
        maxPitchLag = 3 #winodw size for calculating pitch in sec
        maxVocalLag = 3 #winodw size for calculating VTL in sec
        maxPitchVarLag = 10 #window size for calculating pitch var in sec
        
        FormantScatterColors = ['black', 'dimgrey', 'darkgray', 'silver', 'gainsboro', 'whitesmoke']#dot colors for formant scatter plot
        #initialize vars
        meanPitch = 0
        meanTractLength = 0
        stdPitch = 0
        STVarPitch = 0
        
        self.ui.time = np.linspace(0, 1.0 * numSamples / self.ui.fs, numSamples)
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
                    self.ui.time = np.linspace(0, 1.0 * len(self.ui.Recording) / self.ui.fs, len(self.ui.Recording))
                    
                # pull a chunk from our audio stream
                data = PyAudioTest.getChunk(chunkSize, audioStream, Random = 0)   
                data_ds = data[0:chunkSize:ds_rate] # downsample of data
                # its generally a good idea to lowpass filter before downsampling, 
                # but to save computational time this is skipped here.
                # our data is ~mostly~ band-limited, so I don't expect this to be huge problem
                
                # add chunk to our recording
                self.ui.Recording[i * chunkSize:(i + 1) * chunkSize] = data
                
                # get f0 and update f0 plot                
                # use yin implementation
                # yin's original implementation called for filtering, 
                # which we have not yet implemented for computational reasons
                data_hamming = data * np.hamming(chunkSize)
                df = yin.differenceFunction(data_hamming, chunkSize, self.ui.fs/75)
                cmndf = yin.cumulativeMeanNormalizedDifferenceFunction(df, len(df))
                f0 = yin.getPitch(cmndf, self.ui.fs/500, self.ui.fs/75, harmo_th = 0.35) # the value returned is in pitch period samples, not hz
                
                if f0: # if f0 is detected, we have work to do
                    
                    f0 = 1.0 * self.ui.fs/f0 # convert from tau to Hz
                    # store our pitch and time
                    self.ui.Pitch[PitchCount] = f0
                    self.ui.PitchTime[PitchCount] = 1.0 * (t - chunkSize / 2) / self.ui.fs
                    PitchCount += 1
                    # add space if needed so we don't get array out of bounds error
                    if PitchCount >= len(self.ui.PitchTime):
                        self.ui.Pitch = np.concatenate((self.ui.Pitch, np.zeros(200, dtype = np.float32)))
                        self.ui.PitchTime = np.concatenate((self.ui.PitchTime, np.zeros(200, dtype = np.float32)))
                        
                    #get pitches from the last 3 seconds
                    RecentPitches = []
                    pitchIDX = PitchCount - 1
                    while self.ui.PitchTime[pitchIDX] >= 1.0 * (t - chunkSize / 2) / self.ui.fs - maxPitchLag and pitchIDX >= 0:
                        RecentPitches.append(self.ui.Pitch[pitchIDX])
                        pitchIDX -= 1
                        
                    #update f0 bar graph
                    meanPitch = np.mean(RecentPitches)
                    h = self.ui.PitchTarget.value() * 0.01 * 0.5 *self.ui.F0Range.value() # width of target bar
                    h_0 = 3 # width of measurment bar
                    self.f0ax.clear()
                    self.f0ax.hold(True)
                    self.f0ax.bar([0], [2.0 * h], bottom = [self.ui.PitchTarget.value() - h], color = 'aqua')
                    self.f0ax.bar([0], [2.0 * h_0], bottom = [meanPitch - h_0], color = 'black')
                    self.f0ax.set_ylabel('Fundamental Frequency (Hz)')
                    self.f0ax.set_ylim((0, 500))
                    self.f0ax.set_xlim((0, 0.8))
                    self.ui.FundamentalFrequenncyPlot.draw()
                    
                    # get f0 from last 10 seconds for f0 variance
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
                    h = self.ui.VarTarget.value() * 0.01 * 0.5 *self.ui.VarRange.value() # width of target bar
                    h_0 = 0.07 # widht of measurment bar
                    self.VarAx.clear()
                    self.VarAx.hold(True)
                    self.VarAx.bar([0], [2.0 * h], bottom = [self.ui.VarTarget.value() - h], color = 'aqua')
                    self.VarAx.bar([0], [2.0 * h_0], bottom = [STVarPitch - h_0], color = 'black')   
                    self.VarAx.set_ylabel('F0 Variability (Semitones)')
                    self.VarAx.set_ylim((0, 25))
                    self.VarAx.set_xlim((0.0, 0.8))
                    self.ui.PitchVar.draw()
                    
                    if self.ui.PlotStatus == 'F0': # make the autocorrelation graph if we're in F0 mode
                        self.PSDax.clear()
                        self.PSDax.hold(True)
                        x_cmndf = 1.0 * np.array(range(len(cmndf)))
                        x_cmndf = (1.0 * self.ui.fs) / x_cmndf # make abscissa, convert to Hz
                        self.PSDax.plot(x_cmndf, cmndf) # plot difference function
                        self.PSDax.plot([f0, f0], [0, 3], color = 'red') # plot vertical line for F0
                        self.PSDax.plot([0, 500], [0.35, 0.35], color = 'black') # plot horizontal line for threshold
                        self.PSDax.set_title('Mean-normalized Difference Function')
                        self.PSDax.set_xlabel('Frequency (Hz)')
                        self.PSDax.set_ylabel('Mean-normalized Difference')
                        self.PSDax.set_ylim((0, 3))
                        self.PSDax.set_xlim((0, 500))
                        self.ui.PSDPlot.draw()
                        self.PSDax.hold(False)
                    
                if self.ui.PlotStatus == 'Formants':
                    self.PSDax.clear()
                    self.PSDax.hold(True)
                if f0: # if we have F0, look for formants
                    try: # this is in a try block because formant finding can throw errors
                        if self.ui.PlotStatus == 'Formants': # if we're in formants mode, calculate PSD
                            fBins, PSD = sp.signal.periodogram(data_ds, self.ui.fs / ds_rate)
                            PSD = 20 * np.log10(PSD) # convert to dB
                            
                        Formants = FormantFinder.findFormantsLPC(data_ds, self.ui.fs / ds_rate)
                                                
                        #store Formants
                        if len(Formants) >= 5:
                            self.ui.Formants[FormantCount, 0:5] = Formants[0:5]
                        else:
                            self.ui.Formants[FormantCount, 0:len(Formants)] = Formants
                        self.ui.FormantTime[FormantCount] = 1.0 * (t - chunkSize / 2) / self.ui.fs
                        
                        for f in range(len(Formants)): 
                            if self.ui.PlotStatus == 'Formants':
                                self.PSDax.plot([Formants[f], Formants[f]], [-100, 75], color = 'red')# plot the formants as  vertical lines
                            # plot formants as scatter points
                            self.FormantAx.scatter(self.ui.FormantTime[FormantCount], Formants[f], color = FormantScatterColors[f])
                            
                        if self.ui.PlotStatus == 'Formants':  # if we're in formant mode, update our graph  
                            self.PSDax.plot(fBins, PSD)
                            self.PSDax.set_title('Power Spectrum - Formants')
                            self.PSDax.set_xlabel('Frequency (Hz)')
                            self.PSDax.set_ylabel('Power (dB)')
                            self.PSDax.set_ylim((-90, 90))
                            self.PSDax.set_xlim((0, 5000))
                            self.ui.PSDPlot.draw()
                            self.PSDax.hold(False)                        
                        
                        FormantCount += 1
                        # add space if needed to prevent array out of bounds
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
                            
                        # update VTL bar graph
                        meanTractLength = np.median(RecentTractLength)
                        h = self.ui.VTLTarget.value() * 0.01 * 0.5 *self.ui.VTLRange.value() #width for target bar
                        h_0 = 0.2 # width for measurment bar
                        self.tractAx.clear()
                        self.tractAx.hold(True)
                        self.tractAx.bar([0], [2 * h], bottom = [self.ui.VTLTarget.value() - h], color = 'aqua')
                        self.tractAx.bar([0], [2 * h_0], bottom = [meanTractLength - h_0], color = 'black')
                        self.tractAx.set_ylabel('Vocal Tract Length (cm)')
                        self.tractAx.set_ylim((10, 20))
                        self.tractAx.set_xlim((0, 0.8))
                        self.ui.VocalTractPlot.draw()
                            
                    except (RuntimeError): #formant detection can throw errors sometimes
                        Formants = np.zeros(3)
                
                
                #update our raw data plot, but only everyother chunk, because its time consuming
                if t > windowSize * self.ui.fs and i % 3 == 0:
                    self.ax.plot(self.ui.time[t - windowSize * self.ui.fs:t], 
                            self.ui.Recording[t - windowSize * self.ui.fs:t])
                    self.ax.set_title('Raw Waveform')
                    self.ax.set_xlabel('Time (s)')
                    self.ax.set_ylabel('amplitude')
                    self.ui.RawPlot.draw()
                    self.FormantAx.set_ylabel('Frequency (Hz)') # also update our formant scatter plot
                    self.FormantAx.set_xlabel('Time (s)')
                    self.FormantAx.set_ylim((0, 5000))
                    self.FormantAx.set_xlim((t/self.ui.fs - windowSize, t/self.ui.fs + 1))
                    self.ui.FormantPlot.draw()
                    
                    
                #keep track of our target values, in case they chane over time, and also our target ranges
                if i >= len(self.ui.Time): # add extra space to vectors in case we need it to prevent array out of bounds
                    self.ui.Time = np.concatenate((self.ui.Time,  np.zeros(1000, dtype = np.float32)))
                    self.ui.Targets = np.concatenate((self.ui.Targets, np.zeros((1000, 6), dtype = np.float32)))
                    
                self.ui.Time[i] = 1.0 * t / self.ui.fs
                self.ui.Targets[i, 0] = self.ui.PitchTarget.value() 
                self.ui.Targets[i, 1] = self.ui.VTLTarget.value()
                self.ui.Targets[i, 2] = self.ui.VarTarget.value()
                self.ui.Targets[i, 3] = self.ui.PitchTarget.value() * 0.01 * 0.5 * self.ui.F0Range.value()
                self.ui.Targets[i, 4] = self.ui.VTLTarget.value() * 0.01 * 0.5 * self.ui.VTLRange.value()
                self.ui.Targets[i, 5] = self.ui.VarTarget.value() * 0.01 * 0.5 * self.ui.VarRange.value()
                i += 1
                
                #check for incoming button clicks i.e. stop button
                QtCore.QCoreApplication.processEvents()

        except (KeyboardInterrupt, SystemExit): # in case of a keyboard interrupt or system exit, clean house
            self.ui.Rect = RectSelector.PersistRectangleSelector(self.ax, self.SelectArea, # widget for selecting areas
                                       drawtype='box', useblit=False,
                                       button=[1],  # left click only
                                       minspanx=0.1, minspany=0,
                                       spancoords='pixels')
            self.ui.Drag = RectSelector.RectangleAxesDragger(self.ax, self.DragArea, # widget for dragging axes
                                       useblit=False,
                                       button=[3],  # right click only
                                       minspanx=0.5, minspany=0,
                                       spancoords='pixels', parent = self)
            self.ui.RawPlot.draw()
            self.ui.FundamentalFrequenncyPlot.draw()
            #truncate zero pads
            self.ui.Pitch = self.ui.Pitch[0:PitchCount]
            self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
            self.ui.Formants = self.ui.Formants[0:FormantCount, :]
            self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]
            self.ui.Time = self.ui.Time[0:i]
            self.ui.Targets = self.ui.Targets[0:i, :]
            self.ui.Status = False
            print('Recording Completed')
            self.ui.Recording = self.ui.Recording[0:t]
            print('recorded time is')
            print(1.0 * t / self.ui.fs)
            print('elapsed time is:')
            print(ti.time() - start)
            return True            
        
        # clean up at the end of a recording
        self.ui.Rect = RectSelector.PersistRectangleSelector(self.ax, self.SelectArea,
                                       drawtype='box', useblit=False,
                                       button=[1],  # left click only
                                       minspanx=0.1, minspany=0,
                                       spancoords='pixels')  
        self.ui.Drag = RectSelector.RectangleAxesDragger(self.ax, self.DragArea,
                                       useblit=False,
                                       button=[3],  # left click only
                                       minspanx=0.5, minspany=0,
                                       spancoords='pixels', parent = self)
        #truncate zero pads
        self.ui.RawPlot.draw()
        self.ui.Pitch = self.ui.Pitch[0:PitchCount]
        self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
        self.ui.Formants = self.ui.Formants[0:FormantCount, :]
        self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]
        self.ui.Time = self.ui.Time[0:i]
        self.ui.Targets = self.ui.Targets[0:i, :]
        self.ui.Status = False
        print('Recording Completed')
        self.ui.Recording = self.ui.Recording[0:t]
        print('recorded time is')
        print(1.0 * t / self.ui.fs)
        print('elapsed time is:')
        print(ti.time() - start)
        return True
        
    # callback to save recording as .wav
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
            
     # callback to load an existing .wav      
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
        
        # callback for playing old data. See _Go for detailed comments.
    def _Playback(self): # similar to Go, but uses data from Load instead of collecting new data
        
        # make sure we actually have some data loaded
        if np.sum(self.ui.Recording) == 0:
            print('No data loaded, or loaded data is empty. Aborting playback')
            return False
            
        self.ui.Status = True        
        self.ui.Rect = None
        self.ui.Drag = None
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
        self.ui.Targets = np.zeros((1000, 6), dtype = np.float32)
        PitchCount = 0
        FormantCount = 0
        
        self.ax = self.ui.RawPlot.figure.add_subplot(111)
        self.ax.set_title('Raw Waveform')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Amplitude')
        self.PSDax = self.ui.PSDPlot.figure.add_subplot(111)
        self.PSDax.set_title('Power Spectrum')
        self.PSDax.set_xlabel('Frequency (Hz)')
        self.PSDax.set_ylabel('Power')
        
        self.f0ax = self.ui.FundamentalFrequenncyPlot.figure.add_subplot(111)
        self.f0ax.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.f0ax.set_position([0.35, 0.05, 0.6, 0.93])
        self.tractAx = self.ui.VocalTractPlot.figure.add_subplot(111)
        self.tractAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.tractAx.set_position([0.35, 0.05, 0.6, 0.93])
        self.tractAx.set_ylabel('Vocal Tract Length (cm)')
        self.tractAx.set_ylim((10, 20))
        self.tractAx.set_xlim((0, 0.8))
        self.VarAx = self.ui.PitchVar.figure.add_subplot(111)
        self.VarAx.tick_params(
                        axis = 'x',
                        which = 'both',
                        bottom = False,
                        top = False,
                        labelbottom = False)
        self.VarAx.set_position([0.35, 0.05, 0.6, 0.93])
        self.VarAx.set_ylabel('Pitch Variability (Hz)')
        self.VarAx.set_ylim((0, 25))
        self.VarAx.set_xlim((0, 0.8))
        self.FormantAx = self.ui.FormantPlot.figure.add_subplot(111)
        self.FormantAx.clear()
        self.FormantAx.set_ylabel('Frequency (Hz)')
        self.FormantAx.set_xlabel('Time (s)')
        self.FormantAx.set_ylim((0, 5000))
        self.FormantAx.hold(True)
        
        maxPitchLag = 3
        maxVocalLag = 3
        maxPitchVarLag = 10
        meanPitch = 0
        meanTractLength = 0
        stdPitch = 0
        STVarPitch = 0
        FormantScatterColors = ['black', 'dimgrey', 'darkgray', 'silver', 'gainsboro', 'whitesmoke']
        
        ds_rate = 3
        
        c = 34300 # speed of sound in cm/s
        
        self.ui.time = np.linspace(0, 1.0 * numSamples / self.ui.fs, numSamples)
        Count = 0
        t = 0
        print('Beginning Playback')
        try:
            start = ti.time()
            while t < numSamples - chunkSize and self.ui.Status:
                t += chunkSize
                data = PyAudioTest.getChunk(chunkSize, audioStream, Random = 0)
                data = self.ui.Recording[t - chunkSize:t] # replace the data with data from the old recording
                data_ds = data[0:chunkSize:ds_rate] 
                
                # use yin implementation
                data_hamming = data * np.hamming(chunkSize)
                df = yin.differenceFunction(data_hamming, chunkSize, self.ui.fs/75)
                cmndf = yin.cumulativeMeanNormalizedDifferenceFunction(df, len(df))
                f0 = yin.getPitch(cmndf, self.ui.fs/500, self.ui.fs/75, harmo_th = 0.35)
                
                if f0:
                    f0 = 1.0 * self.ui.fs/f0 # convert from tau to Hz
                    # store ot pitch and time
                    self.ui.Pitch[PitchCount] = f0
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
                    h = self.ui.PitchTarget.value() * 0.01 * 0.5 *self.ui.F0Range.value()
                    h_0 = 3
                    self.f0ax.clear()
                    self.f0ax.hold(True)
                    self.f0ax.bar([0], [2.0 * h], bottom = [self.ui.PitchTarget.value() - h], color = 'aqua')
                    self.f0ax.bar([0], [2.0 * h_0], bottom = [meanPitch - h_0], color = 'black')
                    self.f0ax.set_ylabel('Fundamental Frequency (Hz)')
                    self.f0ax.set_ylim((0, 500))
                    self.f0ax.set_xlim((0, 0.8))
                    
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
                        
                    h = self.ui.VarTarget.value() * 0.01 * 0.5 *self.ui.VarRange.value()
                    h_0 = 0.2
                    self.VarAx.clear()
                    self.VarAx.hold(True)
                    self.VarAx.bar([0], [2.0 * h], bottom = [self.ui.VarTarget.value() - h], color = 'aqua')
                    self.VarAx.bar([0], [2.0 * h_0], bottom = [STVarPitch - h_0], color = 'black')   
                    self.VarAx.set_ylabel('F0 Variability (Semitones)')
                    self.VarAx.set_ylim((0, 25))
                    self.VarAx.set_xlim((0.0, 0.8))
                    self.ui.PitchVar.draw()
                    
                    if self.ui.PlotStatus == 'F0':
                        self.PSDax.clear()
                        self.PSDax.hold(True)
                        x_cmndf = 1.0 * np.array(range(len(cmndf)))
                        x_cmndf = (1.0 * self.ui.fs) / x_cmndf
                        self.PSDax.plot(x_cmndf, cmndf)
                        self.PSDax.plot([f0, f0], [0, 3], color = 'red')
                        self.PSDax.plot([0, 500], [0.35, 0.35], color = 'black')
                        self.PSDax.set_title('Mean-normalized Difference Function')
                        self.PSDax.set_xlabel('Frequency (Hz)')
                        self.PSDax.set_ylabel('Mean-normalized Difference')
                        self.PSDax.set_ylim((0, 3))
                        self.PSDax.set_xlim((0, 500))
                        self.ui.PSDPlot.draw()
                        self.PSDax.hold(False)
                          
                if self.ui.PlotStatus == 'Formants':
                    self.PSDax.clear()
                    self.PSDax.hold(True)
                if f0:
                    try:
                        if self.ui.PlotStatus == 'Formants':
                            fBins, PSD = sp.signal.periodogram(data_ds, self.ui.fs / ds_rate)
                            PSD = 20 * np.log10(PSD)
                        Formants = FormantFinder.findFormantsLPC(data_ds, self.ui.fs / ds_rate)
                          
                        
                        
                        if len(Formants) >= 5:
                            self.ui.Formants[FormantCount, 0:5] = Formants[0:5]
                        else:
                            self.ui.Formants[FormantCount, 0:len(Formants)] = Formants
                        self.ui.FormantTime[FormantCount] = 1.0 * (t - chunkSize / 2) / self.ui.fs
                        
                        for f in range(len(Formants)): # plot the formants as  vertical lines
                            if self.ui.PlotStatus == 'Formants':
                                self.PSDax.plot([Formants[f], Formants[f]], [-100, 75], color = 'red')
                            self.FormantAx.scatter(self.ui.FormantTime[FormantCount], Formants[f], color = FormantScatterColors[f])
                            
                        if self.ui.PlotStatus == 'Formants':    
                            self.PSDax.plot(fBins, PSD)
                            self.PSDax.set_title('Power Spectrum - Formants')
                            self.PSDax.set_xlabel('Frequency (Hz)')
                            self.PSDax.set_ylabel('Power (dB)')
                            self.PSDax.set_ylim((-90, 90))
                            self.PSDax.set_xlim((0, 5000))
                            self.ui.PSDPlot.draw()
                            self.PSDax.hold(False)
                            
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
                        h = self.ui.VTLTarget.value() * 0.01 * 0.5 *self.ui.VTLRange.value()
                        h_0 = 0.07
                        self.tractAx.clear()
                        self.tractAx.hold(True)
                        self.tractAx.bar([0], [2 * h], bottom = [self.ui.VTLTarget.value() - h], color = 'aqua')
                        self.tractAx.bar([0], [2 * h_0], bottom = [meanTractLength - h_0], color = 'black')
                        self.tractAx.set_ylabel('Vocal Tract Length (cm)')
                        self.tractAx.set_ylim((10, 20))
                        self.tractAx.set_xlim((0, 0.8))
                        self.ui.VocalTractPlot.draw()
                        
                        
                            
                    except (RuntimeError):
                        Formants = np.zeros(3)
                           
                if t > windowSize * self.ui.fs and Count % 3 == 0:               
                    self.ax.plot(self.ui.time[t - windowSize * self.ui.fs:t], 
                            self.ui.Recording[t - windowSize * self.ui.fs:t])
                    self.ax.set_xlim((t/self.ui.fs - windowSize, t/self.ui.fs + 1))
                    self.ax.set_xlabel('Time (s)')
                    self.ax.set_ylabel('amplitude')
                    self.ax.set_title('Raw Waveform')
                    self.ui.RawPlot.draw()
                    self.FormantAx.set_ylabel('Frequency (Hz)')
                    self.FormantAx.set_xlabel('Time (s)')
                    self.FormantAx.set_ylim((0, 5000))
                    self.FormantAx.set_xlim((t/self.ui.fs - windowSize, t/self.ui.fs + 1))
                    self.ui.FormantPlot.draw()
                
                if Count >= len(self.ui.Time):
                    self.ui.Time = np.concatenate((self.ui.Time,  np.zeros(1000, dtype = np.float32)))
                    self.ui.Targets = np.concatenate((self.ui.Targets, np.zeros((1000, 6), dtype = np.float32)))
                    
                self.ui.Time[Count] = 1.0 * t / self.ui.fs
                self.ui.Targets[Count, 0] = self.ui.PitchTarget.value() 
                self.ui.Targets[Count, 1] = self.ui.VTLTarget.value()
                self.ui.Targets[Count, 2] =self.ui.VarTarget.value()
                self.ui.Targets[Count, 3] = self.ui.PitchTarget.value() * 0.01 * 0.5 * self.ui.F0Range.value()
                self.ui.Targets[Count, 4] = self.ui.VTLTarget.value() * 0.01 * 0.5 * self.ui.VTLRange.value()
                self.ui.Targets[Count, 5] = self.ui.VarTarget.value() * 0.01 * 0.5 * self.ui.VarRange.value()
                
                Count += 1    
                    
                QtCore.QCoreApplication.processEvents()
                    
        except (KeyboardInterrupt, SystemExit):
            self.ui.Rect = RectSelector.PersistRectangleSelector(self.ax, self.SelectArea,
                                       drawtype='box', useblit=False,
                                       button=[1],  # left click only
                                       minspanx=0.1, minspany=0,
                                       spancoords='pixels')
            self.ui.Drag = RectSelector.RectangleAxesDragger(self.ax, self.DragArea,
                                       useblit=False,
                                       button=[3],  # left click only
                                       minspanx=0.5, minspany=0,
                                       spancoords='pixels', parent = self)
            self.ui.RawPlot.draw()
            self.ui.FundamentalFrequenncyPlot.draw()
            self.ui.Pitch = self.ui.Pitch[0:PitchCount]
            self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
            self.ui.Time = self.ui.Time[0:Count]
            self.ui.Targets = self.ui.Targets[0:Count, :]
            self.ui.Formants = self.ui.Formants[0:FormantCount, :]
            self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]
            self.ui.Status = False
            print('Recording Completed')
            print('recorded time is')
            print(1.0 * t / self.ui.fs)
            print('elapsed time is:')
            print(ti.time() - start)
            return True            
            
            
        self.ui.Rect = RectSelector.PersistRectangleSelector(self.ax, self.SelectArea,
                                       drawtype='box', useblit=False,
                                       button=[1],  # left click only
                                       minspanx=0.1, minspany=0,
                                       spancoords='pixels') 
        self.ui.Drag = RectSelector.RectangleAxesDragger(self.ax, self.DragArea,
                                       useblit=False,
                                       button=[3],  # left click only
                                       minspanx=0.5, minspany=0,
                                       spancoords='pixels', parent = self)
        self.ui.RawPlot.draw()
        self.ui.Pitch = self.ui.Pitch[0:PitchCount]
        self.ui.PitchTime = self.ui.PitchTime[0:PitchCount]
        self.ui.Time = self.ui.Time[0:Count]
        self.ui.Targets = self.ui.Targets[0:Count, :]
        self.ui.Formants = self.ui.Formants[0:FormantCount, :]
        self.ui.FormantTime = self.ui.FormantTime[0:FormantCount]
        self.ui.Status = False        
        print('Recording Completed')
        print('recorded time is')
        print(1.0 * t / self.ui.fs)
        print('elapsed time is:')
        print(ti.time() - start)
    
    # callback for the axes dragger
    def DragArea(self, eclick, erelease):
        # re-initialize the dragger widget.
        self.ui.Drag = RectSelector.RectangleAxesDragger(self.ax, self.DragArea,
                                       useblit=False,
                                       button=[3],  # right click only
                                       minspanx=0.5, minspany=0,
                                       spancoords='pixels', parent = self)
        
    # callback for selecting an area
    def SelectArea(self, eclick, erelease):
        if not self.ui.Status:
            # call the line selectro callback
            RectSelector.line_select_callback(eclick, erelease, parent = self)
            # convert coordinates of box to time
            tMin = np.min((self.Coords[0], self.Coords[2]))
            tMax = np.max((self.Coords[0], self.Coords[2]))
            
            SelectedPitch = []
            SelectedVTL = []
            # get pitch and VTL from selected ares
            for i in range(len(self.ui.PitchTime)):
                if self.ui.PitchTime[i] > tMin and self.ui.PitchTime[i] < tMax:
                    SelectedPitch.append(self.ui.Pitch[i])

            for i in range(len(self.ui.FormantTime)):
                if self.ui.FormantTime[i] > tMin and self.ui.FormantTime[i] < tMax:
                    vtl = FormantFinder.getVocalTractLength(self.ui.Formants[i, :], method = 'lammert')
                    if vtl > 9 and vtl < 25: 
                        SelectedVTL.append(vtl)
            # if at least one pitch is selected, update our mean pitch plot. otherwise, clear it.           
            if len(SelectedPitch) > 0:
                meanPitch = np.mean(SelectedPitch)
                h = self.ui.PitchTarget.value() * 0.01 * 0.5 *self.ui.F0Range.value()
                h_0 = 3
                self.f0ax.clear()
                self.f0ax.hold(True)
                self.f0ax.bar([0], [2.0 * h], bottom = [self.ui.PitchTarget.value() - h], color = 'aqua')
                self.f0ax.bar([0], [2.0 * h_0], bottom = [meanPitch - h_0], color = 'black')
                self.f0ax.set_ylabel('Fundamental Frequency (Hz)')
                self.f0ax.set_ylim((0, 500))
                self.f0ax.set_xlim((0, 0.8))
            else:
                self.f0ax.clear()
                self.f0ax.set_ylabel('Fundamental Frequency (Hz)')
                self.f0ax.set_ylim((0, 500))
                self.f0ax.set_xlim((0, 0.8))
                self.ui.FundamentalFrequenncyPlot.draw()
            # repeat for VTL
            if len(SelectedVTL) > 0:
                meanVTL = np.mean(SelectedVTL)
                h = self.ui.VTLTarget.value() * 0.01 * 0.5 *self.ui.VTLRange.value()
                h_0 = 0.07
                self.tractAx.clear()
                self.tractAx.hold(True)
                self.tractAx.bar([0], [2 * h], bottom = [self.ui.VTLTarget.value() - h], color = 'aqua')
                self.tractAx.bar([0], [2 * h_0], bottom = [meanVTL - h_0], color = 'black')
                self.tractAx.set_ylabel('Vocal Tract Length (cm)')
                self.tractAx.set_ylim((10, 20))
                self.tractAx.set_xlim((0, 0.8))
                self.ui.VocalTractPlot.draw()
            else:
                self.tractAx.clear()
                self.tractAx.set_ylabel('Fundamental Frequency (Hz)')
                self.tractAx.set_ylim((0, 500))
                self.tractAx.set_xlim((0, 0.8))
                self.ui.VocalTractPlot.draw()
                
            # repeat for pitch variance, except we need at least 2 samples.
            if len(SelectedPitch) > 1:
                RPitch = 39.86 * np.log10(SelectedPitch / meanPitch)
                STVarPitch = np.std(RPitch)
                h = self.ui.VarTarget.value() * 0.01 * 0.5 *self.ui.VarRange.value()
                h_0 = 0.2
                self.VarAx.clear()
                self.VarAx.hold(True)
                self.VarAx.bar([0], [2.0 * h], bottom = [self.ui.VarTarget.value() - h], color = 'aqua')
                self.VarAx.bar([0], [2.0 * h_0], bottom = [STVarPitch - h_0], color = 'black')   
                self.VarAx.set_ylabel('F0 Variability (Semitones)')
                self.VarAx.set_ylim((0, 25))
                self.VarAx.set_xlim((0.0, 0.8))
                self.ui.PitchVar.draw()
            else:
                self.VarAx.clear()
                self.VarAx.set_ylabel('F0 Variability (Semitones)')
                self.VarAx.set_ylim((0, 25))
                self.VarAx.set_xlim((0.0, 0.8))
                self.ui.PitchVar.draw()
            
            # convert tmin and tmax to indices
            idxMin = np.round(tMin * self.ui.fs)
            idxMax = np.round(tMax * self.ui.fs)
            
            if idxMin < 0: #prevent array out of bounds errors
                idxMin = 0
            if idxMax > len(self.ui.Recording):
                idxMax = len(self.ui.Recording)
            if idxMax < 0: #prevent array out of bounds errors
                idxMax = 0
            if idxMin > len(self.ui.Recording):
                idxMin = len(self.ui.Recording)

            # get PSD from the selected region
            if not idxMin == idxMax:
                selectedData = self.ui.Recording[idxMin:idxMax]
                fBins, PSD = sp.signal.periodogram(selectedData, self.ui.fs)
                PSD = 20 * np.log10(PSD)
                self.PSDax.clear()
                self.PSDax.plot(fBins, PSD)
                self.PSDax.set_title('Power Spectrum - Formants')
                self.PSDax.set_xlabel('Frequency (Hz)')
                self.PSDax.set_ylabel('Power (dB)')
                self.PSDax.set_ylim((-90, 90))
                self.PSDax.set_xlim((0, 5000))
                self.ui.PSDPlot.draw()
            else:
                self.PSDax.clear()
                self.PSDax.set_title('Power Spectrum - Formants')
                self.PSDax.set_xlabel('Frequency (Hz)')
                self.PSDax.set_ylabel('Power (dB)')
                self.PSDax.set_ylim((-90, 90))
                self.PSDax.set_xlim((0, 5000))
                self.ui.PSDPlot.draw()

        
def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()