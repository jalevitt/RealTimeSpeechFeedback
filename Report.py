# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:06:10 2020

@author: Josh Levitt
"""

# Form implementation generated from reading ui file 'Documents\RealTimeSpeechFeedback-working\Report.ui'
#
# Created: Mon Mar 23 10:06:03 2020
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
        MainWindow.resize(760, 743)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.RawPlot = MatplotlibWidget(self.centralwidget)
        self.RawPlot.setGeometry(QtCore.QRect(10, 60, 531, 161))
        self.RawPlot.setObjectName(_fromUtf8("RawPlot"))
        self.PitchPlot = MatplotlibWidget(self.centralwidget)
        self.PitchPlot.setGeometry(QtCore.QRect(10, 230, 531, 161))
        self.PitchPlot.setObjectName(_fromUtf8("PitchPlot"))
        self.VTLPlot = MatplotlibWidget(self.centralwidget)
        self.VTLPlot.setGeometry(QtCore.QRect(10, 400, 531, 161))
        self.VTLPlot.setObjectName(_fromUtf8("VTLPlot"))
        self.VarPlot = MatplotlibWidget(self.centralwidget)
        self.VarPlot.setGeometry(QtCore.QRect(10, 570, 531, 161))
        self.VarPlot.setObjectName(_fromUtf8("VarPlot"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(550, 60, 93, 28))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(550, 90, 93, 28))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        #MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 760, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))

from matplotlibwidget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
