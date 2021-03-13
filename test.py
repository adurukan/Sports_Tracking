from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QRect, QCoreApplication, QMetaObject
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QPushButton, QMenuBar, QMenu, QStatusBar, QAction, QFileDialog


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(80, 70, 641, 301))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton_1 = QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QRect(170, 380, 93, 28))
        self.pushButton_1.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/play_arrow-24px.svg"), QIcon.Normal, QIcon.Off)
        self.pushButton_1.setIcon(icon)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(80, 380, 93, 28))
        self.pushButton_2.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("icons/fast_rewind-24px.svg"), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QRect(250, 380, 93, 28))
        self.pushButton_3.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("icons/pause-24px.svg"), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QRect(340, 380, 93, 28))
        self.pushButton_4.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap("icons/fast_forward-24px.svg"), QIcon.Normal, QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QRect(630, 380, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_1.clicked.connect(self.play)
        self.pushButton_3.clicked.connect(self.stop)
        MainWindow.setCentralWidget(self.centralwidget)

        self.verticalLayout.addWidget(videoWidget)
        self.mediaPlayer.setVideoOutput(videoWidget)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.load_video)

        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def load_video(self):
        fileName, _ = QFileDialog.getOpenFileName(self, " ",
                                                  ".", "Video Files (*.mp4 *.avi)")
        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            #self.playButton.setEnabled(True)
            #self.statusBar.showMessage(fileName)
            #self.play()
    def play(self):
        if self.mediaPlayer.state() != QMediaPlayer.PlayingState:
            self.mediaPlayer.play()

    def stop(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_5.setText(_translate("MainWindow", "Tracker"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
