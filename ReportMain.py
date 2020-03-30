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
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.ui = Report.Ui_MainWindow()
        self.ui.setupUi(self)

        self.Coords = (0, 0, 0, 0)
        maxPitchLag = 3
        maxVTLLag = 5
        maxVarLag = 10
        
        n = len(parent.ui.Recording)
        Time = np.linspace(0, 1.0 * n/parent.ui.fs, n)
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
        
        self.Rect = RectSelector.PersistRectangleSelector(self.ax, self.RawLineCallbackWrapper,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels')

        self.ui.RawPlot.show()
        
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
                
        self.f0ax = self.ui.PitchPlot.figure.add_subplot(111)
        self.f0ax.set_position([0.12, 0.25, 0.85, 0.63])
        self.f0ax.hold(True)
        self.f0ax.plot(parent.ui.Time, parent.ui.Targets[:, 0], color = 'black')
        self.f0ax.scatter(parent.ui.PitchTime, Pitch)
        self.f0ax.set_ylim((0, 500))
        self.f0ax.set_xlim((0, 1.0 * n/parent.ui.fs))
        self.f0ax.set_title('Pitch')
        self.f0ax.set_ylabel('Pitch (Hz)')
        self.f0ax.set_xlabel('Time (s)')
        self.ui.PitchPlot.show()
        
        VTL = np.zeros(parent.ui.FormantTime.shape)
        for i in range(len(parent.ui.FormantTime)):
            t = parent.ui.FormantTime[i]
            RecentVTL = []
            idx = 0
            while i - idx >=0 and t - parent.ui.FormantTime[i - idx] <= maxVTLLag:
                vtl = FormantFinder.getVocalTractLength(parent.ui.Formants[i - idx, :], method = 'lammert')
                if vtl > 9 and vtl < 25:
                    RecentVTL.append(vtl)
                idx += 1
                
            if len(RecentVTL) > 0:
                VTL[i] = np.mean(RecentVTL)
            else:
                VTL[i] = np.nan
                
        self.VTLax = self.ui.VTLPlot.figure.add_subplot(111)
        self.VTLax.set_position([0.12, 0.25, 0.85, 0.63])
        self.VTLax.hold(True)
        self.VTLax.plot(parent.ui.Time, parent.ui.Targets[:, 1], color = 'black')
        self.VTLax.scatter(parent.ui.FormantTime, VTL)
        self.VTLax.set_ylim((0, 25))
        self.VTLax.set_xlim((0, 1.0 * n/parent.ui.fs))
        self.VTLax.set_title('Vocal Tract Length')
        self.VTLax.set_ylabel('Vocal Tract Length (cm)')
        self.VTLax.set_xlabel('Time (s)')
        self.ui.VTLPlot.show()
        
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
                Var[i] = np.std(39.86 * np.log10(np.array(RecentVar)/m))
            else:
                Var[i] = np.nan
        
        self.VarAx = self.ui.VarPlot.figure.add_subplot(111)
        self.VarAx.set_position([0.12, 0.25, 0.85, 0.63])
        self.VarAx.hold(True)
        self.VarAx.plot(parent.ui.Time, parent.ui.Targets[:, 2], color = 'black')
        self.VarAx.scatter(parent.ui.PitchTime, Var)
        self.VarAx.set_ylim((0, 25))
        self.VarAx.set_xlim((0, 1.0 * n/parent.ui.fs))
        self.VarAx.set_title('Pitch Variability')
        self.VarAx.set_ylabel('Pitch Variability (Hz)')
        self.VarAx.set_xlabel('Time (s)')
        self.ui.VarPlot.show()
        
        D = 1.0 * n/parent.ui.fs
        MP = np.nanmean(Pitch)
        MVTL = np.nanmean(VTL)
        MPV = np.nanmean(Var)
        RecordingStats = """
 Duration:                   %05.1f seconds
 Mean Pitch:                 %05.1f Hz
 Mean Vocal Tract Length:    %05.2f cm
 Mean Pitch Variability:     %05.2f st        
        """ %(D, MP, MVTL, MPV)
        self.ui.RecordingText.setText(RecordingStats)
        
        self.Var = Var
        self.Pitch = Pitch
        self.VTL = VTL
        
        self.ui.PlayBack.clicked.connect(self._PlayCallback)
        
    def RawLineCallbackWrapper(self, eclick, erelease):
        self.RawLineCallback(eclick, erelease)



        
    def RawLineCallback(self, eclick, erelease):
        
        #[p.remove() for p in reversed(self.ax.patches)]
        RectSelector.line_select_callback(eclick, erelease, parent = self)
        self.ax.clear()
        n = len(self.parent.ui.Recording)
        Time = np.linspace(0, 1.0 * n/self.parent.ui.fs, n)
        self.ax = self.ui.RawPlot.figure.add_subplot(111)
        self.ax.set_position([0.12, 0.25, 0.85, 0.63])
        self.ax.plot(Time, self.parent.ui.Recording)
        self.ax.set_title('Raw Waveform')
        self.ax.set_ylabel('Amplitude')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_xlim((0, 1.0 * n/self.parent.ui.fs))
        self.ax.tick_params(
                        axis = 'y',
                        which = 'both',
                        left = False,
                        right = False,
                        labelleft = False)
        
        
        
        self.Rect = RectSelector.PersistRectangleSelector(self.ax, self.RawLineCallbackWrapper,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels')
        self.ui.RawPlot.show()
            

        
        
        
    def _PlayCallback(self):
        tMin = round(self.parent.ui.fs * np.min((self.Coords[0], self.Coords[2])))
        tMax = round(self.parent.ui.fs * np.max((self.Coords[0], self.Coords[2])))
        Data = self.parent.ui.Recording[tMin:tMax]
        wavFile = wave.open('temp.wav', 'w')
        wavFile.setnchannels(1)
        wavFile.setsampwidth(2)
        wavFile.setframerate(self.parent.ui.fs)
        #write data to file        
        wavFile.writeframesraw(np.ndarray.tobytes(Data))
        #close everything
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
        os.remove('temp.wav')

                
        

