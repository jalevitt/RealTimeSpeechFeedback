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
        '''
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)


        # set the layout
        layout = QtGui.QVBoxLayout()

        layout.addWidget(self.canvas)
        self.setLayout(layout)
        '''
        self.Coords = (0, 0, 0, 0)
        maxPitchLag = 3
        maxVTLLag = 5
        maxVarLag = 10
        
        n = len(parent.ui.Recording)
        Time = np.linspace(0, 1.0 * n/parent.ui.fs, n)
        ax = self.ui.RawPlot.figure.add_subplot(111)
        ax.set_position([0.12, 0.25, 0.85, 0.63])
        ax.plot(Time, parent.ui.Recording)
        ax.set_title('Raw Waveform')
        ax.set_ylabel('Amplitude')
        ax.set_xlabel('Time (s)')
        ax.set_xlim((0, 1.0 * n/parent.ui.fs))
        ax.tick_params(
                        axis = 'y',
                        which = 'both',
                        left = False,
                        right = False,
                        labelleft = False)
        
        self.Rect = RectSelector.RectangleSelector(ax, self.RawLineCallback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels')
        self.RawRect = patches.Rectangle((0, 0), 0, 0, fill = False)
        '''
        self.ui.RawPlot.connect('key_press_event', RectSelector.toggle_selector)
        '''
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
                
        f0ax = self.ui.PitchPlot.figure.add_subplot(111)
        f0ax.set_position([0.12, 0.25, 0.85, 0.63])
        f0ax.hold(True)
        f0ax.plot((0, 1.0 * n/parent.ui.fs), 
                (parent.ui.PitchTarget.value(), parent.ui.PitchTarget.value()), 
                 color = 'black')
        f0ax.scatter(parent.ui.PitchTime, Pitch)
        f0ax.set_ylim((0, 500))
        f0ax.set_xlim((0, 1.0 * n/parent.ui.fs))
        f0ax.set_title('Pitch')
        f0ax.set_ylabel('Pitch (Hz)')
        f0ax.set_xlabel('Time (s)')
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
                
        VTLax = self.ui.VTLPlot.figure.add_subplot(111)
        VTLax.set_position([0.12, 0.25, 0.85, 0.63])
        VTLax.hold(True)
        VTLax.plot((0, 1.0 * n/parent.ui.fs), 
                   (parent.ui.VTLTarget.value(), parent.ui.VTLTarget.value()), 
                    color = 'black')
        VTLax.scatter(parent.ui.FormantTime, VTL)
        VTLax.set_ylim((0, 25))
        VTLax.set_xlim((0, 1.0 * n/parent.ui.fs))
        VTLax.set_title('Vocal Tract Length')
        VTLax.set_ylabel('Vocal Tract Length (cm)')
        VTLax.set_xlabel('Time (s)')
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
                Var[i] = np.std(RecentVar)
            else:
                Var[i] = np.nan
        
        VarAx = self.ui.VarPlot.figure.add_subplot(111)
        VarAx.set_position([0.12, 0.25, 0.85, 0.63])
        VarAx.hold(True)
        VarAx.plot((0, 1.0 * n/parent.ui.fs), 
                   (parent.ui.VarTarget.value(), parent.ui.VarTarget.value()), 
                    color = 'black')
        VarAx.scatter(parent.ui.PitchTime, Var)
        VarAx.set_ylim((0, 40))
        VarAx.set_xlim((0, 1.0 * n/parent.ui.fs))
        VarAx.set_title('Pitch Variability')
        VarAx.set_ylabel('Pitch Variability (Hz)')
        VarAx.set_xlabel('Time (s)')
        self.ui.VarPlot.show()
        
        self.ui.PlayBack.clicked.connect(self._PlayCallback)
        
    def RawLineCallback(self, eclick, erelease):
        RectSelector.line_select_callback(eclick, erelease, parent = self)
        self.RawRect = patches.Rectangle((np.min((self.Coords[0], self.Coords[2])), 
                                         np.min((self.Coords[1], self.Coords[3]))),
                                        np.abs(self.Coords[0] - self.Coords[2]),
                                        np.abs(self.Coords[0] - self.Coords[2]),
                                        fill = False,
                                        ec = 'black',
                                        figure = self.ui.RawPlot)

        #self.RawRect.set_height(np.abs(self.Coords[1] - self.Coords[3]))
        #self.RawRect.set_width(np.abs(self.Coords[0] - self.Coords[2]))
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

                
        

