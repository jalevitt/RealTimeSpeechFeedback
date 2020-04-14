# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:11:04 2020

@author: Josh Levitt
"""

from PyQt4 import QtCore, QtGui
import Report
import numpy as np
import FormantFinder
import RectSelector
from matplotlib import patches
import pyaudio
import time
import wave
import os


class ReportWindow(QtGui.QDialog):
    def __init__(self,parent = None):
        # open the ui
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.ui = Report.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # set some parameters
        self.Coords = (0, 0, 0, 0)
        maxPitchLag = 3
        maxVTLLag = 5
        maxVarLag = 10
        
        # build time abscisa 
        n = len(parent.ui.Recording)
        Time = np.linspace(0, 1.0 * n/parent.ui.fs, n)
        
        # set up waveform plot
        self.ax = self.ui.RawPlot.figure.add_subplot(111)
        self.ax.set_position([0.12, 0.25, 0.85, 0.63])
        self.ax.plot(Time, parent.ui.Recording)
        self.ax.set_title('Raw Waveform')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_xlim((0, 1.0 * n/parent.ui.fs))
        self.ax.tick_params(
                        axis = 'y',
                        which = 'both',
                        left = False,
                        right = False,
                        labelleft = False)
        # set up rectangle selector widget
        self.Rect = RectSelector.PersistRectangleSelector(self.ax, self.RawLineCallbackWrapper,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=0.1, minspany=0,
                                       spancoords='pixels')

        self.ui.RawPlot.show()
        
        # use mean-smoothing method to calculate pitch
        Pitch = np.zeros(parent.ui.PitchTime.shape)
        for i in range(len(parent.ui.PitchTime)):
            t = parent.ui.PitchTime[i]
            RecentPitches = []
            idx = 0
            while i - idx >=0 and t - parent.ui.PitchTime[i - idx] <= maxPitchLag:
                RecentPitches.append(parent.ui.Pitch[i-idx])
                idx += 1
            if len(RecentPitches) > 0:
                Pitch[i] = np.mean(RecentPitches)
            else:
                Pitch[i] = np.nan
        # build pitch graph  
        self.f0ax = self.ui.PitchPlot.figure.add_subplot(111)
        self.f0ax.set_position([0.12, 0.25, 0.85, 0.63])
        self.f0ax.hold(True)
        self.f0ax.plot(parent.ui.Time, parent.ui.Targets[:, 0], color = 'aqua')
        self.f0ax.plot(parent.ui.Time, parent.ui.Targets[:, 0] + parent.ui.Targets[:, 3], color = 'aqua', linestyle = 'dashed')
        self.f0ax.plot(parent.ui.Time, parent.ui.Targets[:, 0] - parent.ui.Targets[:, 3], color = 'aqua', linestyle = 'dashed')
        self.f0ax.scatter(parent.ui.PitchTime, Pitch, color = 'black')
        self.f0ax.set_ylim((0, 500))
        self.f0ax.set_xlim((0, 1.0 * n/parent.ui.fs))
        self.f0ax.set_title('Fundemental Frequency')
        self.f0ax.set_ylabel('Fundemental Frequency (Hz)')
        self.f0ax.set_xlabel('Time (s)')
        self.ui.PitchPlot.show()
        
        # use mean smoothing to calculate VTL
        VTL = np.zeros(parent.ui.FormantTime.shape)
        for i in range(len(parent.ui.FormantTime)):
            t = parent.ui.FormantTime[i]
            RecentVTL = []
            idx = 0
            while i - idx >=0 and t - parent.ui.FormantTime[i - idx] <= maxVTLLag:
                vtl = FormantFinder.getVocalTractLength(parent.ui.Formants[i - idx, :], method = 'lammert')
                if vtl > 9 and vtl < 25: # exclude implausible VTL
                    RecentVTL.append(vtl)
                idx += 1
                
            if len(RecentVTL) > 0:
                VTL[i] = np.mean(RecentVTL)
            else:
                VTL[i] = np.nan
        # plot VTL   
        self.VTLax = self.ui.VTLPlot.figure.add_subplot(111)
        self.VTLax.set_position([0.12, 0.25, 0.85, 0.63])
        self.VTLax.hold(True)
        self.VTLax.plot(parent.ui.Time, parent.ui.Targets[:, 1], color = 'aqua')
        self.VTLax.plot(parent.ui.Time, parent.ui.Targets[:, 1] + parent.ui.Targets[:, 4], color = 'aqua', linestyle = 'dashed')
        self.VTLax.plot(parent.ui.Time, parent.ui.Targets[:, 1] - parent.ui.Targets[:, 4], color = 'aqua', linestyle = 'dashed')
        self.VTLax.scatter(parent.ui.FormantTime, VTL,  color = 'black')
        self.VTLax.set_ylim((0, 25))
        self.VTLax.set_xlim((0, 1.0 * n/parent.ui.fs))
        self.VTLax.set_title('Vocal Tract Length')
        self.VTLax.set_ylabel('Vocal Tract Length (cm)')
        self.VTLax.set_xlabel('Time (s)')
        self.ui.VTLPlot.show()
        
        # use 10 second window to calc pitch variability
        Var = np.zeros(parent.ui.PitchTime.shape)
        for i in range(len(parent.ui.PitchTime)):
            t = parent.ui.PitchTime[i]
            RecentVar = []
            idx = 0
            while i - idx >=0 and t - parent.ui.PitchTime[i - idx] <= maxVarLag:
                RecentVar.append(parent.ui.Pitch[i-idx])
                idx += 1
            if len(RecentVar) > 1:
                m = np.mean(RecentVar)               
                Var[i] = np.std(39.86 * np.log10(np.array(RecentVar)/m)) # convert to semitones
            else:
                Var[i] = np.nan
                
        # build variability plot
        self.VarAx = self.ui.VarPlot.figure.add_subplot(111)
        self.VarAx.set_position([0.12, 0.25, 0.85, 0.63])
        self.VarAx.hold(True)
        self.VarAx.plot(parent.ui.Time, parent.ui.Targets[:, 2], color = 'aqua')
        self.VarAx.plot(parent.ui.Time, parent.ui.Targets[:, 2] + parent.ui.Targets[:, 5], color = 'aqua', linestyle = 'dashed')
        self.VarAx.plot(parent.ui.Time, parent.ui.Targets[:, 2] - parent.ui.Targets[:, 5], color = 'aqua', linestyle = 'dashed')
        self.VarAx.scatter(parent.ui.PitchTime, Var,  color = 'black')
        self.VarAx.set_ylim((0, 25))
        self.VarAx.set_xlim((0, 1.0 * n/parent.ui.fs))
        self.VarAx.set_title('F0 Variability')
        self.VarAx.set_ylabel('Fundemental Frequency Variability (st)')
        self.VarAx.set_xlabel('Time (s)')
        self.ui.VarPlot.show()
        
        # calculate variables for text area
        D = 1.0 * n/parent.ui.fs
        MP = np.nanmean(Pitch)
        MVTL = np.nanmean(VTL)
        MPV = np.nanmean(Var)
        # set text
        RecordingStats = """
 Duration:                   %05.1f seconds
 Mean Fundemental Frequency: %05.1f Hz
 Mean Vocal Tract Length:    %05.2f cm
 Mean F0 Variability:        %05.2f st        
        """ %(D, MP, MVTL, MPV)
        self.ui.RecordingText.setText(RecordingStats)
        
        # store variables
        self.Var = Var
        self.Pitch = Pitch
        self.VTL = VTL
        
        self.ui.PlayBack.clicked.connect(self._PlayCallback)
        
        # just a wrapper function, not strictly necessary
    def RawLineCallbackWrapper(self, eclick, erelease):
        self.RawLineCallback(eclick, erelease)



        # this is the function called by the wrapper. this is the business.
    def RawLineCallback(self, eclick, erelease):
        
        # call the line selectro callback
        RectSelector.line_select_callback(eclick, erelease, parent = self)

        # calculate variables for text area
        tMin = np.min((self.Coords[0], self.Coords[2]))
        tMax = np.max((self.Coords[0], self.Coords[2]))
        pitch_t_min_idx = 0
        pitch_t_max_idx = 0
        for i in range(len(self.parent.ui.PitchTime)): # first get pitches in the selected area
            if self.parent.ui.PitchTime[i] > tMin and pitch_t_min_idx == 0:
                pitch_t_min_idx = i
            if self.parent.ui.PitchTime[i] < tMax:
                pitch_t_max_idx = i
        VTL_t_min_idx = 0
        VTL_t_max_idx = 0
        for i in range(len(self.parent.ui.FormantTime)): # then get VTL in the selected area
            if self.parent.ui.FormantTime[i] > tMin and VTL_t_min_idx == 0:
                VTL_t_min_idx = i
            if self.parent.ui.FormantTime[i] < tMax:
                VTL_t_max_idx = i
        
        PitchSelection = self.Pitch[pitch_t_min_idx:pitch_t_max_idx + 1]
        VarSelection = self.Var[pitch_t_min_idx:pitch_t_max_idx + 1]
        VTLSelection = self.VTL[VTL_t_min_idx:VTL_t_max_idx + 1]
        
        # calculate the size of the selection, and the means of the variables
        D = tMax - tMin 
        MP = np.nanmean(PitchSelection)
        MVTL = np.nanmean(VTLSelection)
        MPV = np.nanmean(VarSelection)
        
        # set text
        RecordingStats = """
 Selected Time:             (%05.1f, %05.1f)
 Duration:                   %05.1f seconds
 Mean Fundemental Frequency: %05.1f Hz
 Mean Vocal Tract Length:    %05.2f cm
 Mean F0 Variability:        %05.2f st        
        """ %(tMin, tMax, D, MP, MVTL, MPV)
        self.ui.SelectionText.setText(RecordingStats)
        
        
        # callback for playing a selected area
    def _PlayCallback(self):
        # get the times we want to play
        tMin = round(self.parent.ui.fs * np.min((self.Coords[0], self.Coords[2])))
        tMax = round(self.parent.ui.fs * np.max((self.Coords[0], self.Coords[2])))
        Data = self.parent.ui.Recording[tMin:tMax]
        
        # write the data to to temporary .wav file so we can play it
        wavFile = wave.open('temp.wav', 'w')
        wavFile.setnchannels(1)
        wavFile.setsampwidth(2)
        wavFile.setframerate(self.parent.ui.fs)
        #write data to file        
        wavFile.writeframesraw(np.ndarray.tobytes(Data))
        #close the writing stream
        wavFile.close()
        
        
        CHUNK = 1024    
        wf = wave.open('temp.wav', 'rb')

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()
        
        # open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        # read data
        data = wf.readframes(CHUNK)
        
        # play stream (3)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)
        
        # stop stream (4)
        stream.stop_stream()
        stream.close()
        
        # close PyAudio (5)
        p.terminate()
        wf.close()
        
        # remove our temporary .wav file
        os.remove('temp.wav')

                
        

