# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 21:08:22 2021

@author: erdem and alpay
"""

#Imports
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtWidgets import QFileDialog, QGraphicsOpacityEffect
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
import os.path
from gui import Ui_MainWindow
import cv2

#Init
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

#Init MediaPlayer
ui.video_frame = QtWidgets.QLabel()
ui.videoLayout.addWidget(ui.video_frame)
ui.video_frame.setScaledContents(1)
x_motion = ui.motion.x()
y_motion = ui.motion.y()

# creating a opacity effect
ui.opacity_effect = QGraphicsOpacityEffect()
# setting opacity level
ui.opacity_effect.setOpacity(0.4)
# adding opacity effect to the label
ui.motion.setGraphicsEffect(ui.opacity_effect)

transform = QtGui.QTransform()

#Trial Sequance   
def script():
    from track import tracking
    loaded = tracking.loadFile(fileName)

    if loaded:
        frame, pt2, pt3, w1 ,h1  = tracking.mapping()
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
        pix = QtGui.QPixmap.fromImage(img)
        ui.video_frame.setPixmap(pix)

        #Move and Scale the image of field
        wref = pt3[0]-pt2[0]
        href = pt3[1]-pt2[1]
        ui.motion.move(int(ui.motion.x()+pt2[0]), int(ui.motion.y() + pt2[1]))
        transform.scale(wref/ w1,href/ h1)

        cond = True
        while cond:
            if playing:
                frame, tracking_frame= tracking.running()

                #Turn the frame into an image
                img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
                pix = QtGui.QPixmap.fromImage(img)
                ui.video_frame.setPixmap(pix)
                QtTest.QTest.qWait(1)
                cv2.destroyWindow("select")

                #Reconstruct image on the transformed position
                img2 = QtGui.QImage(tracking_frame, tracking_frame.shape[1], tracking_frame.shape[0],tracking_frame.strides[0], QtGui.QImage.Format_BGR888)
                pix2 = QtGui.QPixmap.fromImage(img2)
                pix2 = QtGui.QPixmap(pix2.transformed(transform))

                ui.motion.setPixmap(pix2)
            else:
                QtTest.QTest.qWait(0.001)


#Multimedia Functions
def load_video():
    global fileName, playing
    fileName, _ = QFileDialog.getOpenFileName(None, " ",
                                              ".", "Video Files (*.mp4 *.avi)")
    playing = True

def play():
    global playing
    playing = True

def pause():
    global playing
    playing = False

#Trigger
ui.load.clicked.connect(lambda: load_video())
ui.start.clicked.connect(lambda: script())
ui.play.clicked.connect(lambda: play())
ui.pause.clicked.connect(lambda: pause())

sys.exit(app.exec_())


