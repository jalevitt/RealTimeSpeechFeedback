# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Documents\RealTimeSpeechFeedback-working\DeveloperUI.ui'
#
# Created: Mon Apr 20 10:19:51 2020
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(909, 766)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.SavePitch = QtGui.QPushButton(self.centralwidget)
        self.SavePitch.setObjectName(_fromUtf8("SavePitch"))
        self.gridLayout_3.addWidget(self.SavePitch, 6, 5, 1, 1)
        self.RawPlot = MatplotlibWidget(self.centralwidget)
        self.RawPlot.setObjectName(_fromUtf8("RawPlot"))
        self.gridLayout_3.addWidget(self.RawPlot, 1, 1, 1, 6)
        self.PitchVar = MatplotlibWidget(self.centralwidget)
        self.PitchVar.setObjectName(_fromUtf8("PitchVar"))
        self.gridLayout_3.addWidget(self.PitchVar, 1, 15, 1, 5)
        self.Stop = QtGui.QPushButton(self.centralwidget)
        self.Stop.setObjectName(_fromUtf8("Stop"))
        self.gridLayout_3.addWidget(self.Stop, 4, 4, 1, 1)
        self.UserMode = QtGui.QPushButton(self.centralwidget)
        self.UserMode.setObjectName(_fromUtf8("UserMode"))
        self.gridLayout_3.addWidget(self.UserMode, 6, 2, 1, 1)
        self.VarTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VarTarget.setMaximum(100.0)
        self.VarTarget.setProperty("value", 15.0)
        self.VarTarget.setObjectName(_fromUtf8("VarTarget"))
        self.gridLayout_3.addWidget(self.VarTarget, 4, 17, 1, 2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 2, 16, 2, 3)
        self.PlotSpectrogram = QtGui.QPushButton(self.centralwidget)
        self.PlotSpectrogram.setObjectName(_fromUtf8("PlotSpectrogram"))
        self.gridLayout_3.addWidget(self.PlotSpectrogram, 5, 3, 2, 1)
        self.Save = QtGui.QPushButton(self.centralwidget)
        self.Save.setObjectName(_fromUtf8("Save"))
        self.gridLayout_3.addWidget(self.Save, 3, 5, 1, 1)
        self.FundamentalFrequenncyPlot = MatplotlibWidget(self.centralwidget)
        self.FundamentalFrequenncyPlot.setObjectName(_fromUtf8("FundamentalFrequenncyPlot"))
        self.gridLayout_3.addWidget(self.FundamentalFrequenncyPlot, 1, 7, 1, 4)
        self.VarRange = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VarRange.setMaximum(100.0)
        self.VarRange.setProperty("value", 10.0)
        self.VarRange.setObjectName(_fromUtf8("VarRange"))
        self.gridLayout_3.addWidget(self.VarRange, 6, 17, 1, 2)
        self.Go = QtGui.QPushButton(self.centralwidget)
        self.Go.setObjectName(_fromUtf8("Go"))
        self.gridLayout_3.addWidget(self.Go, 3, 4, 1, 1)
        self.VTLRange = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VTLRange.setMaximum(100.0)
        self.VTLRange.setProperty("value", 10.0)
        self.VTLRange.setObjectName(_fromUtf8("VTLRange"))
        self.gridLayout_3.addWidget(self.VTLRange, 6, 13, 1, 1)
        self.ReportButton = QtGui.QPushButton(self.centralwidget)
        self.ReportButton.setObjectName(_fromUtf8("ReportButton"))
        self.gridLayout_3.addWidget(self.ReportButton, 4, 3, 1, 1)
        self.PlayBack = QtGui.QPushButton(self.centralwidget)
        self.PlayBack.setObjectName(_fromUtf8("PlayBack"))
        self.gridLayout_3.addWidget(self.PlayBack, 3, 3, 1, 1)
        self.LoadData = QtGui.QPushButton(self.centralwidget)
        self.LoadData.setObjectName(_fromUtf8("LoadData"))
        self.gridLayout_3.addWidget(self.LoadData, 3, 2, 1, 1)
        self.VocalTractPlot = MatplotlibWidget(self.centralwidget)
        self.VocalTractPlot.setObjectName(_fromUtf8("VocalTractPlot"))
        self.gridLayout_3.addWidget(self.VocalTractPlot, 1, 11, 1, 4)
        self.SaveFormants = QtGui.QPushButton(self.centralwidget)
        self.SaveFormants.setObjectName(_fromUtf8("SaveFormants"))
        self.gridLayout_3.addWidget(self.SaveFormants, 4, 5, 1, 1)
        self.VTLTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VTLTarget.setMaximum(25.0)
        self.VTLTarget.setProperty("value", 15.0)
        self.VTLTarget.setObjectName(_fromUtf8("VTLTarget"))
        self.gridLayout_3.addWidget(self.VTLTarget, 4, 13, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 6, 6, 1, 3)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 2, 8, 2, 2)
        self.F0Range = QtGui.QDoubleSpinBox(self.centralwidget)
        self.F0Range.setMaximum(100.0)
        self.F0Range.setProperty("value", 10.0)
        self.F0Range.setObjectName(_fromUtf8("F0Range"))
        self.gridLayout_3.addWidget(self.F0Range, 6, 9, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 2, 12, 2, 2)
        self.FormantPlot = MatplotlibWidget(self.centralwidget)
        self.FormantPlot.setObjectName(_fromUtf8("FormantPlot"))
        self.gridLayout_3.addWidget(self.FormantPlot, 7, 1, 3, 6)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.PSDPlot = MatplotlibWidget(self.centralwidget)
        self.PSDPlot.setObjectName(_fromUtf8("PSDPlot"))
        self.gridLayout_3.addWidget(self.PSDPlot, 7, 7, 3, 12)
        self.PlotSwitch = QtGui.QPushButton(self.centralwidget)
        self.PlotSwitch.setObjectName(_fromUtf8("PlotSwitch"))
        self.gridLayout_3.addWidget(self.PlotSwitch, 7, 18, 1, 1)
        self.PitchTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.PitchTarget.setMaximum(500.0)
        self.PitchTarget.setProperty("value", 100.0)
        self.PitchTarget.setObjectName(_fromUtf8("PitchTarget"))
        self.gridLayout_3.addWidget(self.PitchTarget, 4, 9, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 909, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.myCallback = QtGui.QAction(MainWindow)
        self.myCallback.setObjectName(_fromUtf8("myCallback"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.SavePitch.setText(_translate("MainWindow", "Save F0", None))
        self.Stop.setText(_translate("MainWindow", "Stop", None))
        self.UserMode.setText(_translate("MainWindow", "User Mode", None))
        self.label_3.setText(_translate("MainWindow", "Target F0\n"
"Variability (st)", None))
        self.PlotSpectrogram.setText(_translate("MainWindow", "Plot Spectrogram", None))
        self.Save.setText(_translate("MainWindow", "Save .wav", None))
        self.Go.setText(_translate("MainWindow", "Go", None))
        self.ReportButton.setText(_translate("MainWindow", "Generate Report", None))
        self.PlayBack.setText(_translate("MainWindow", "Playback Recording", None))
        self.LoadData.setText(_translate("MainWindow", "Load Existing Data", None))
        self.SaveFormants.setText(_translate("MainWindow", "Save Formants", None))
        self.label_4.setText(_translate("MainWindow", "Range (%)", None))
        self.label.setText(_translate("MainWindow", "Target Fundemental\n"
"Frequency (Hz)", None))
        self.label_2.setText(_translate("MainWindow", "Target Vocal \n"
"Tract Length (cm)", None))
        self.PlotSwitch.setText(_translate("MainWindow", "Switch Mode", None))
        self.myCallback.setText(_translate("MainWindow", "Test", None))

from matplotlibwidget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())