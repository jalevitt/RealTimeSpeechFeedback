# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Documents\RealTimeSpeechFeedback-working\UserUI.ui'
#
# Created: Mon Apr 20 10:19:06 2020
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
        MainWindow.resize(975, 528)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 8, 21)
        self.TwoD = MatplotlibWidget(self.centralwidget)
        self.TwoD.setObjectName(_fromUtf8("TwoD"))
        self.gridLayout_4.addWidget(self.TwoD, 1, 1, 1, 5)
        self.FundamentalFrequenncyPlot = MatplotlibWidget(self.centralwidget)
        self.FundamentalFrequenncyPlot.setObjectName(_fromUtf8("FundamentalFrequenncyPlot"))
        self.gridLayout_4.addWidget(self.FundamentalFrequenncyPlot, 1, 6, 1, 5)
        self.VocalTractPlot = MatplotlibWidget(self.centralwidget)
        self.VocalTractPlot.setObjectName(_fromUtf8("VocalTractPlot"))
        self.gridLayout_4.addWidget(self.VocalTractPlot, 1, 11, 1, 4)
        self.PitchVar = MatplotlibWidget(self.centralwidget)
        self.PitchVar.setObjectName(_fromUtf8("PitchVar"))
        self.gridLayout_4.addWidget(self.PitchVar, 1, 15, 1, 6)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 2, 7, 2, 3)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 2, 12, 2, 4)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 2, 17, 2, 3)
        self.LoadData = QtGui.QPushButton(self.centralwidget)
        self.LoadData.setObjectName(_fromUtf8("LoadData"))
        self.gridLayout_4.addWidget(self.LoadData, 3, 1, 2, 1)
        self.PlayBack = QtGui.QPushButton(self.centralwidget)
        self.PlayBack.setObjectName(_fromUtf8("PlayBack"))
        self.gridLayout_4.addWidget(self.PlayBack, 3, 2, 2, 1)
        self.Go = QtGui.QPushButton(self.centralwidget)
        self.Go.setObjectName(_fromUtf8("Go"))
        self.gridLayout_4.addWidget(self.Go, 3, 3, 2, 1)
        self.Save = QtGui.QPushButton(self.centralwidget)
        self.Save.setObjectName(_fromUtf8("Save"))
        self.gridLayout_4.addWidget(self.Save, 3, 4, 2, 1)
        self.PitchTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.PitchTarget.setMaximum(500.0)
        self.PitchTarget.setProperty("value", 100.0)
        self.PitchTarget.setObjectName(_fromUtf8("PitchTarget"))
        self.gridLayout_4.addWidget(self.PitchTarget, 4, 8, 2, 1)
        self.VTLTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VTLTarget.setMaximum(25.0)
        self.VTLTarget.setProperty("value", 15.0)
        self.VTLTarget.setObjectName(_fromUtf8("VTLTarget"))
        self.gridLayout_4.addWidget(self.VTLTarget, 4, 13, 2, 1)
        self.VarTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VarTarget.setMaximum(100.0)
        self.VarTarget.setProperty("value", 15.0)
        self.VarTarget.setObjectName(_fromUtf8("VarTarget"))
        self.gridLayout_4.addWidget(self.VarTarget, 4, 18, 2, 1)
        self.ReportButton = QtGui.QPushButton(self.centralwidget)
        self.ReportButton.setObjectName(_fromUtf8("ReportButton"))
        self.gridLayout_4.addWidget(self.ReportButton, 5, 2, 1, 1)
        self.Stop = QtGui.QPushButton(self.centralwidget)
        self.Stop.setObjectName(_fromUtf8("Stop"))
        self.gridLayout_4.addWidget(self.Stop, 5, 3, 2, 1)
        self.SaveFormants = QtGui.QPushButton(self.centralwidget)
        self.SaveFormants.setObjectName(_fromUtf8("SaveFormants"))
        self.gridLayout_4.addWidget(self.SaveFormants, 5, 4, 2, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 6, 5, 2, 3)
        self.F0Range = QtGui.QDoubleSpinBox(self.centralwidget)
        self.F0Range.setMaximum(100.0)
        self.F0Range.setProperty("value", 10.0)
        self.F0Range.setObjectName(_fromUtf8("F0Range"))
        self.gridLayout_4.addWidget(self.F0Range, 6, 8, 2, 1)
        self.VTLRange = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VTLRange.setMaximum(100.0)
        self.VTLRange.setProperty("value", 10.0)
        self.VTLRange.setObjectName(_fromUtf8("VTLRange"))
        self.gridLayout_4.addWidget(self.VTLRange, 6, 13, 2, 1)
        self.VarRange = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VarRange.setMaximum(100.0)
        self.VarRange.setProperty("value", 10.0)
        self.VarRange.setObjectName(_fromUtf8("VarRange"))
        self.gridLayout_4.addWidget(self.VarRange, 6, 18, 2, 1)
        self.DevMode = QtGui.QPushButton(self.centralwidget)
        self.DevMode.setObjectName(_fromUtf8("DevMode"))
        self.gridLayout_4.addWidget(self.DevMode, 7, 1, 1, 1)
        self.SavePitch = QtGui.QPushButton(self.centralwidget)
        self.SavePitch.setObjectName(_fromUtf8("SavePitch"))
        self.gridLayout_4.addWidget(self.SavePitch, 7, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 975, 26))
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
        self.label.setText(_translate("MainWindow", "Target Fundemental\n"
"Frequency (Hz)", None))
        self.label_2.setText(_translate("MainWindow", "Target Vocal \n"
"Tract Length (cm)", None))
        self.label_3.setText(_translate("MainWindow", "Target F0\n"
"Variability (st)", None))
        self.LoadData.setText(_translate("MainWindow", "Load Existing Data", None))
        self.PlayBack.setText(_translate("MainWindow", "Playback Recording", None))
        self.Go.setText(_translate("MainWindow", "Go", None))
        self.Save.setText(_translate("MainWindow", "Save .wav", None))
        self.ReportButton.setText(_translate("MainWindow", "Generate Report", None))
        self.Stop.setText(_translate("MainWindow", "Stop", None))
        self.SaveFormants.setText(_translate("MainWindow", "Save Formants", None))
        self.label_4.setText(_translate("MainWindow", "Range (%)", None))
        self.DevMode.setText(_translate("MainWindow", "Developer Mode", None))
        self.SavePitch.setText(_translate("MainWindow", "Save F0", None))
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