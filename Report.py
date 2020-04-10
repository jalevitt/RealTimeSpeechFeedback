# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Documents\RealTimeSpeechFeedback-working\Report.ui'
#
# Created: Mon Mar 30 16:16:39 2020
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
        MainWindow.resize(830, 784)
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
        self.PlayBack = QtGui.QPushButton(self.centralwidget)
        self.PlayBack.setGeometry(QtCore.QRect(550, 60, 93, 28))
        self.PlayBack.setObjectName(_fromUtf8("PlayBack"))
        self.RecordingText = QtGui.QTextBrowser(self.centralwidget)
        self.RecordingText.setGeometry(QtCore.QRect(550, 130, 256, 231))
        self.RecordingText.setObjectName(_fromUtf8("RecordingText"))
        self.SelectionText = QtGui.QTextBrowser(self.centralwidget)
        self.SelectionText.setGeometry(QtCore.QRect(550, 410, 256, 231))
        self.SelectionText.setObjectName(_fromUtf8("SelectionText"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 390, 131, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 110, 141, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        #MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 830, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.PlayBack.setText(_translate("MainWindow", "Play Selection", None))
        self.RecordingText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))
        self.label.setText(_translate("MainWindow", "Selection Statistics", None))
        self.label_2.setText(_translate("MainWindow", "Recording Statistics", None))

from matplotlibwidget import MatplotlibWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())