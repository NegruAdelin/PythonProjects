from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QColor, QImage
from PyQt5.QtWidgets import  QWidget, QFileDialog, QColorDialog
import cv2

def distanta(color):
    global culoare1
    return abs(culoare1.red() - color[0]) + abs(culoare1.green() - color[1]) + abs(culoare1.blue() - color[2])

def procesare(slideVal):
    global culoare2, imagineAux, imagine
    h, w, _ = imagine.shape

    for i in range(h):
        for j in range(w):
            if(distanta(imagine[i, j]) < slideVal):
                imagineAux[i, j][0] = culoare2.red()
                imagineAux[i, j][1] = culoare2.green()
                imagineAux[i, j][2] = culoare2.blue()
            else:
                imagineAux[i, j] = imagine[i, j]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.AlegeImaginea = QtWidgets.QPushButton(self.centralwidget)
        self.AlegeImaginea.setGeometry(QtCore.QRect(20, 20, 131, 41))
        self.AlegeImaginea.setObjectName("AlegeImaginea")
        self.AlegeImaginea.clicked.connect(self.getImage)

        self.Culori = QtWidgets.QPushButton(self.centralwidget)
        self.Culori.setGeometry(QtCore.QRect(20, 80, 131, 41))
        self.Culori.setObjectName("Culori")
        self.Culori.clicked.connect(self.clickedCulori)

        self.Target = QtWidgets.QSlider(self.centralwidget)
        self.Target.setGeometry(QtCore.QRect(50, 140, 22, 181))
        self.Target.setOrientation(QtCore.Qt.Vertical)
        self.Target.setObjectName("Target")
        self.Target.setMinimum(0)
        self.Target.setMaximum(255)
        self.Target.valueChanged.connect(self.slideMiscat)

        self.Min = QtWidgets.QLabel(self.centralwidget)
        self.Min.setGeometry(QtCore.QRect(90, 300, 47, 13))
        self.Min.setText("")
        self.Min.setObjectName("Min")
        self.Min.setNum(0)

        self.Max = QtWidgets.QLabel(self.centralwidget)
        self.Max.setGeometry(QtCore.QRect(90, 140, 47, 13))
        self.Max.setText("")
        self.Max.setObjectName("Max")
        self.Max.setNum(255)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 110, 441, 351))
        self.label.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.label.setText("")
        self.label.setObjectName("label")

        self.Mesaj = QtWidgets.QLabel(self.centralwidget)
        self.Mesaj.setGeometry(QtCore.QRect(260, 20, 431, 31))
        self.Mesaj.setStyleSheet("font: 75 12pt \"Courier New\";")
        self.Mesaj.setText("")
        self.Mesaj.setObjectName("Mesaj")

        self.Salveaza = QtWidgets.QPushButton(self.centralwidget)
        self.Salveaza.setGeometry(QtCore.QRect(20, 370, 131, 41))
        self.Salveaza.setObjectName("Salveaza")
        self.Salveaza.clicked.connect(self.clickedSalveaza)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AlegeImaginea.setText(_translate("MainWindow", "Alege Imaginea"))
        self.Culori.setText(_translate("MainWindow", "Culori"))
        self.Salveaza.setText(_translate("MainWindow", "Salveaza"))

    def getImage(self):
        global imagineAux, imagine, nameOfSavedFile

        filePath, _ = QFileDialog.getOpenFileName()
        nameOfSavedFile = filePath
        pixmap = QPixmap(filePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.label.resize(pixmap.width(), pixmap.height())
        imagine = cv2.imread(filePath)
        imagine = cv2.cvtColor(imagine, cv2.COLOR_BGR2RGB)

    def slideMiscat(self):
        global imagineAux
        imagineAux = imagine.copy()
        self.Min.setNum(self.Target.value())
        slideVal = self.Target.value()
        procesare(slideVal)
        h, w, c = imagineAux.shape
        img = QImage(imagineAux.data, w, h, QImage.Format_RGB888)
        pixmap = QPixmap(img)
        self.label.setPixmap(QPixmap(pixmap))

    def clickedCulori(self):
        global culoare1, culoare2
        culoare1 = QColorDialog.getColor()
        culoare2 = QColorDialog.getColor()

    def clickedSalveaza(self):
        global imagineAux, nameOfSavedFile
        nameOfSavedFile = nameOfSavedFile[0:len(nameOfSavedFile) - 4] + "Test" + nameOfSavedFile[len(nameOfSavedFile) - 4:len(nameOfSavedFile)]

        imagineAux = cv2.cvtColor(imagineAux, cv2.COLOR_BGR2RGB)
        if(cv2.imwrite(nameOfSavedFile, imagineAux)):
            self.Mesaj.setText("Imaginea a fost salvata")

        imagineAux = cv2.cvtColor(imagineAux, cv2.COLOR_BGR2RGB)

        cv2.waitKey(2000)
        self.Mesaj.setText("")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    waitKey()


culoare1 = culoare2 = imagine = imagineAux = nameOfSavedFile = ""