import wave, contextlib, math
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

############################
#UI made with QTDesigner
class Ui_VideoTranscriber(object):
    def __init__(self):
        self.mp4FileName = ""
        self.outputFileName = ""
        self.audioFileName = "defaultaudio.wav"
        
    def setupUi(self, VideoTranscriber):
        VideoTranscriber.setObjectName("VideoTranscriber")
        VideoTranscriber.resize(880, 800)
        self.centralwidget = QtWidgets.QWidget(VideoTranscriber)
        self.centralwidget.setObjectName("centralwidget")
        
        #transcribed text space
        self.transcribedTextBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.transcribedTextBox.setGeometry(QtCore.QRect(40, 220, 801, 441))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.transcribedTextBox.setFont(font)
        self.transcribedTextBox.setObjectName("transcribedTextBox")
        
        #open file button
        self.openFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.openFileButton.setGeometry(QtCore.QRect(310, 10, 90, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.openFileButton.setFont(font)
        self.openFileButton.setObjectName("openFileButton")
        self.openFileButton.clicked.connect(self.openFileFunction)
        
        #selected file button
        self.selectedFile = QtWidgets.QLabel(self.centralwidget)
        self.selectedFile.setGeometry(QtCore.QRect(270, 690, 521, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectedFile.setFont(font)
        self.selectedFile.setAutoFillBackground(True)
        self.selectedFile.setFrameShape(QtWidgets.QFrame.Box)
        self.selectedFile.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.selectedFile.setText("")
        self.selectedFile.setObjectName("selectedFile")
        
        #display/input output file name
        self.outputFile = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.outputFile.setGeometry(QtCore.QRect(270, 60, 531, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outputFile.setFont(font)
        self.outputFile.setObjectName("outputFile")
        
        #some labels
        self.LABELselectedfile = QtWidgets.QLabel(self.centralwidget)
        self.LABELselectedfile.setGeometry(QtCore.QRect(40, 690, 180, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LABELselectedfile.setFont(font)
        self.LABELselectedfile.setObjectName("LABELselectedfile")
        self.LABELoutputname = QtWidgets.QLabel(self.centralwidget)
        self.LABELoutputname.setGeometry(QtCore.QRect(40, 60, 180, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.LABELoutputname.setFont(font)
        self.LABELoutputname.setObjectName("LABELoutputname")
        self.LABELTRANCSCRIPTION = QtWidgets.QLabel(self.centralwidget)
        self.LABELTRANCSCRIPTION.setGeometry(QtCore.QRect(300, 160, 280, 40))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.LABELTRANCSCRIPTION.setFont(font)
        self.LABELTRANCSCRIPTION.setAlignment(QtCore.Qt.AlignCenter)
        self.LABELTRANCSCRIPTION.setObjectName("LABELTRANCSCRIPTION")
        
        #status update bar
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(40, 110, 800, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.statusLabel.setFont(font)
        self.statusLabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.statusLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName("statusLabel")
        
        #start transcription button
        self.startTranscribeButton = QtWidgets.QPushButton(self.centralwidget)
        self.startTranscribeButton.setGeometry(QtCore.QRect(470, 10, 150, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.startTranscribeButton.setFont(font)
        self.startTranscribeButton.setObjectName("startTranscribeButton")
        self.startTranscribeButton.clicked.connect(self.startTranscriptionFunction)
        self.startTranscribeButton.setEnabled(False)
        
        #window options
        VideoTranscriber.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VideoTranscriber)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 880, 26))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuRefresh = QtWidgets.QMenu(self.menubar)
        self.menuRefresh.setObjectName("menuRefresh")
        VideoTranscriber.setMenuBar(self.menubar)
        self.menuabout = QtWidgets.QAction(VideoTranscriber)
        self.menurefresh = QtWidgets.QAction(VideoTranscriber)
        self.statusbar = QtWidgets.QStatusBar(VideoTranscriber)
        self.statusbar.setObjectName("statusbar")
        VideoTranscriber.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(VideoTranscriber)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered.connect(self.showAboutFunction)
        self.menuAbout.addAction(self.actionAbout)
        self.actionRefresh = QtWidgets.QAction(VideoTranscriber)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRefresh.triggered.connect(self.refreshFunction)
        self.menuRefresh.addAction(self.actionRefresh)
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuRefresh.menuAction())
        self.retranslateUi(VideoTranscriber)
        QtCore.QMetaObject.connectSlotsByName(VideoTranscriber)
        
    #UI stuff
    def retranslateUi(self, VideoTranscriber):
        _translate = QtCore.QCoreApplication.translate
        VideoTranscriber.setWindowTitle(_translate("VideoTranscriber", "Video Transcriber Tool"))
        self.transcribedTextBox.setPlaceholderText(_translate("VideoTranscriber", "Your transcription will go here"))
        self.openFileButton.setText(_translate("VideoTranscriber", "Open File"))
        self.outputFile.setPlaceholderText(_translate("VideoTranscriber", "Insert name of text file that will be generated here"))
        self.LABELselectedfile.setText(_translate("VideoTranscriber", "Selected file"))
        self.LABELoutputname.setText(_translate("VideoTranscriber", "Output name"))
        self.LABELTRANCSCRIPTION.setText(_translate("VideoTranscriber", "Transcription:"))
        self.statusLabel.setText(_translate("VideoTranscriber", "Welcome to our video transcribing tool! Waiting for inputs...."))
        self.startTranscribeButton.setText(_translate("VideoTranscriber", "Start transcription"))
        self.menuAbout.setTitle(_translate("VideoTranscriber", "Video Transcriber"))
        self.actionAbout.setText(_translate("VideoTranscriber", "About us"))
        self.menuRefresh.setTitle(_translate("VideoTranscriber", "Refresh"))
        self.actionRefresh.setText(_translate("VideoTranscriber", "Click to refresh"))
 
    #function for choosing files you want converted       
    def openFileFunction(self):
        filename = QFileDialog.getOpenFileName()
        if filename[0][-3:] == "mp4":
            self.startTranscribeButton.setEnabled(True)
            self.mp4FileName = filename[0]
            self.statusLabel.setText("File succesfully received. Click to start transcription")
            self.selectedFile.setText(filename[0])
        else:
            self.selectedFile.setText("")
            self.statusLabel.setText("Only .mp4 files can be converted")

#############################################################

#Lexer
    #function to start mp4 file to .wav before conversion 
    def convertFileFunction(self):
        self.statusLabel.setText("Converting .mp4 file to .wav ....")
        self.convert_thread = convertVideoToAudioThread(self.mp4FileName, self.audioFileName)
        self.convert_thread.finished.connect(self.conversionEnd)
        self.convert_thread.start()
    
    #function to get duration of audio, so that it can be divided to words
    def getAudioDurationFunction(self, audioFileName):
        with contextlib.closing(wave.open(audioFileName,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
##############################################################

#Parser (continued down below)     
    #function for audio transcription 
    def transcribeAudioFunction(self, audioFileName):
        totalduration = self.getAudioDurationFunction(audioFileName) / 10
        totalduration = math.ceil(totalduration)
        self.td = totalduration
        if len(self.outputFile.toPlainText()) > 0:
            self.outputFileName = self.outputFile.toPlainText()
        else:
            self.outputFileName = "defaulttranscription.txt"
        self.thread = transcriptionThread(totalduration, audioFileName, self.outputFileName)
        self.thread.finished.connect(self.transcriptionEnd)
        self.thread.change_value.connect(self.setStatusProgressFunction)
        self.thread.start()
        
###############################################################
    
    #update UI when conversion ends and starting transcription
    def conversionEnd(self):
        self.statusLabel.setText("File conversion done, starting transcription....")
        self.transcribeAudioFunction(self.audioFileName)
    
    #update UI when transcription ends
    def transcriptionEnd(self):
        self.startTranscribeButton.setEnabled(True)
        self.statusLabel.setText("Transcription finished. Displaying results")
        self.updateOutputFunction()
        
    #function to start transcription
    def startTranscriptionFunction(self):
        self.startTranscribeButton.setEnabled(False)
        self.transcribedTextBox.setText("")
        self.convertFileFunction()
        
    #updating status label 
    def setStatusProgressFunction(self, val): 
        increment = int(math.floor(100*(float(val)/self.td)))
        self.statusLabel.setText(("Transcription status: "+str(increment)+"%"))
        
    #function that updates the text box
    def updateOutputFunction(self):
        f = open(self.outputFileName, "r")
        self.transcribedTextBox.setText(f.read())
        f.close()
    
    #function to refresh app
    def refreshFunction(self):
        self.statusLabel.setText("Waiting for inputs....")
        self.transcribedTextBox.setText("")
        self.selectedFile.setText("")
        self.outputFile.document().setPlainText("")
    
    #function for show about button
    def showAboutFunction(self):
        msg = QMessageBox()
        msg.setWindowTitle("Video Transcriber Tool")
        msg.setText(" Made by Ariel, Rafian and Rendy")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

#using threads so performance improves and app does not freeze
class convertVideoToAudioThread(QThread):
    def __init__(self, mp4FileName, audioFileName):
        QThread.__init__(self)
        self.mp4FileName = mp4FileName
        self.audioFileName = audioFileName
    def __del__(self):
        self.wait()
    def run(self):
        audioclip = AudioFileClip(self.mp4FileName)
        audioclip.write_audiofile(self.audioFileName)

#continuation of parser where we use google Web Speech API to match the words
class transcriptionThread(QThread):
    change_value = pyqtSignal(int)
    def __init__(self, totalduration, audioFileName, outputFileName):
        QThread.__init__(self)
        self.totalduration = totalduration
        self.audioFileName = audioFileName
        self.outputFileName = outputFileName
    def __del__(self):
        self.wait()
    def run(self):
        r = sr.Recognizer()
        missingwordcount = 0
        for i in range(0, self.totalduration):
            try:
                with sr.AudioFile(self.audioFileName) as source:
                    audio = r.record(source, offset=i*10, duration=10)
                    f = open(self.outputFileName, "a")
                    f.write(r.recognize_google(audio))
                    f.write(" ")
                self.change_value.emit(i)
            except:
                missingwordcount += 1
                print("Skipping unknown word....")
                continue
            f.close()
        print("Skipped words:", missingwordcount, "words")

#main to run UI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VideoTranscriber = QtWidgets.QMainWindow()
    ui = Ui_VideoTranscriber()
    ui.setupUi(VideoTranscriber)
    VideoTranscriber.show()
    sys.exit(app.exec_())