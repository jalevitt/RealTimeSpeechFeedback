# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Documents\RealTimeSpeechFeedback-working\DeveloperUI.ui'
#
# Created: Tue Mar 31 14:06:26 2020
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
        MainWindow.resize(1046, 762)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.RawPlot = MatplotlibWidget(self.centralwidget)
        self.RawPlot.setGeometry(QtCore.QRect(10, 10, 521, 421))
        self.RawPlot.setObjectName(_fromUtf8("RawPlot"))
        self.Go = QtGui.QPushButton(self.centralwidget)
        self.Go.setGeometry(QtCore.QRect(260, 440, 75, 23))
        self.Go.setObjectName(_fromUtf8("Go"))
        self.LoadData = QtGui.QPushButton(self.centralwidget)
        self.LoadData.setGeometry(QtCore.QRect(10, 440, 111, 23))
        self.LoadData.setObjectName(_fromUtf8("LoadData"))
        self.PlayBack = QtGui.QPushButton(self.centralwidget)
        self.PlayBack.setGeometry(QtCore.QRect(130, 440, 121, 23))
        self.PlayBack.setObjectName(_fromUtf8("PlayBack"))
        self.Save = QtGui.QPushButton(self.centralwidget)
        self.Save.setGeometry(QtCore.QRect(340, 440, 111, 23))
        self.Save.setObjectName(_fromUtf8("Save"))
        self.FundamentalFrequenncyPlot = MatplotlibWidget(self.centralwidget)
        self.FundamentalFrequenncyPlot.setGeometry(QtCore.QRect(540, 10, 141, 301))
        self.FundamentalFrequenncyPlot.setObjectName(_fromUtf8("FundamentalFrequenncyPlot"))
        self.Stop = QtGui.QPushButton(self.centralwidget)
        self.Stop.setGeometry(QtCore.QRect(260, 470, 75, 23))
        self.Stop.setObjectName(_fromUtf8("Stop"))
        self.SaveFormants = QtGui.QPushButton(self.centralwidget)
        self.SaveFormants.setGeometry(QtCore.QRect(340, 470, 111, 23))
        self.SaveFormants.setObjectName(_fromUtf8("SaveFormants"))
        self.SavePitch = QtGui.QPushButton(self.centralwidget)
        self.SavePitch.setGeometry(QtCore.QRect(340, 500, 111, 23))
        self.SavePitch.setObjectName(_fromUtf8("SavePitch"))
        self.VocalTractPlot = MatplotlibWidget(self.centralwidget)
        self.VocalTractPlot.setGeometry(QtCore.QRect(690, 10, 141, 301))
        self.VocalTractPlot.setObjectName(_fromUtf8("VocalTractPlot"))
        self.PitchVar = MatplotlibWidget(self.centralwidget)
        self.PitchVar.setGeometry(QtCore.QRect(839, 10, 141, 301))
        self.PitchVar.setObjectName(_fromUtf8("PitchVar"))
        self.UserMode = QtGui.QPushButton(self.centralwidget)
        self.UserMode.setGeometry(QtCore.QRect(10, 500, 111, 21))
        self.UserMode.setObjectName(_fromUtf8("UserMode"))
        self.PitchTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.PitchTarget.setGeometry(QtCore.QRect(570, 360, 62, 22))
        self.PitchTarget.setMaximum(500.0)
        self.PitchTarget.setProperty("value", 100.0)
        self.PitchTarget.setObjectName(_fromUtf8("PitchTarget"))
        self.VTLTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VTLTarget.setGeometry(QtCore.QRect(710, 360, 62, 22))
        self.VTLTarget.setMaximum(25.0)
        self.VTLTarget.setProperty("value", 15.0)
        self.VTLTarget.setObjectName(_fromUtf8("VTLTarget"))
        self.VarTarget = QtGui.QDoubleSpinBox(self.centralwidget)
        self.VarTarget.setGeometry(QtCore.QRect(870, 360, 62, 22))
        self.VarTarget.setMaximum(100.0)
        self.VarTarget.setProperty("value", 15.0)
        self.VarTarget.setObjectName(_fromUtf8("VarTarget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 330, 101, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(700, 320, 121, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(860, 320, 91, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.ReportButton = QtGui.QPushButton(self.centralwidget)
        self.ReportButton.setGeometry(QtCore.QRect(130, 470, 121, 21))
        self.ReportButton.setObjectName(_fromUtf8("ReportButton"))
        self.PSDPlot = MatplotlibWidget(self.centralwidget)
        self.PSDPlot.setGeometry(QtCore.QRect(540, 390, 441, 321))
        self.PSDPlot.setObjectName(_fromUtf8("PSDPlot"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1046, 26))
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
        self.Go.setText(_translate("MainWindow", "Go", None))
        self.LoadData.setText(_translate("MainWindow", "Load Existing Data", None))
        self.PlayBack.setText(_translate("MainWindow", "Playback Recording", None))
        self.Save.setText(_translate("MainWindow", "Save .wav", None))
        self.Stop.setText(_translate("MainWindow", "Stop", None))
        self.SaveFormants.setText(_translate("MainWindow", "Save Formants", None))
        self.SavePitch.setText(_translate("MainWindow", "Save Pitch", None))
        self.UserMode.setText(_translate("MainWindow", "User Mode", None))
        self.label.setText(_translate("MainWindow", "Target Pitch (Hz)", None))
        self.label_2.setText(_translate("MainWindow", "Target Vocal \n"
"Tract Length (cm)", None))
        self.label_3.setText(_translate("MainWindow", "Target Pitch\n"
"Variability (st)", None))
        self.ReportButton.setText(_translate("MainWindow", "Generate Report", None))
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