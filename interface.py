import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon, QPixmap

import scipy
from scipy.fftpack import dctn, idctn
from scipy import misc
import numpy as np
import math
import os
import matplotlib.pyplot as mplp


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Metodi del calcolo Scientifico'
        self.left = 10
        self.top = 10
        self.width = 1080
        self.height = 960
        self.file_path = None
        self.textboxValue_f = 0
        self.textboxValue_d = 0
        self.first_original = True
        self.first_compress = True
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.button_carica = QPushButton('Carica immagine', self)
        self.button_carica.setToolTip('Carica immagine')
        self.button_carica.move(176,46)
        self.button_carica.clicked.connect(self.on_click_carica)

        # Create textox for f
        self.text_f = QLabel(self)
        self.text_f.setText('Insert F:')
        self.textbox_f = QLineEdit(self, placeholderText="")
        self.textbox_f.move(180, 100)
        self.textbox_f.resize(150,40)
        self.text_f.move(120, 110)

        # Create textbox for d
        self.text_d = QLabel(self)
        self.text_d.setText('Insert D = 0 to (2F − 2)')
        self.textbox_d = QLineEdit(self, placeholderText="")
        self.textbox_d.move(180, 150)
        self.textbox_d.resize(150,40)
        self.text_d.move(20, 160)

        # connect button to function on_click_d_f
        # Create a button in the window
        self.button_d_f = QPushButton('Esegui', self)
        self.button_d_f.move(175,210)
        self.button_d_f.clicked.connect(self.on_click_d_f)

        #self.saveFileDialog()
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open", "","bmp Files (*.bmp);;All Files (*)", options=options)
        return(fileName)

    @pyqtSlot()
    def on_click_carica(self):
        fileName = self.openFileNameDialog()
        self.file_path = fileName
        if(self.first_original != True):
            self.immage_original.clear()
        else:
            self.first_original = False
        
        if(self.first_compress != True):
            self.immage_compress.hide()
        else:
            self.first_compress = False
        
        self.immage_original = QLabel(self)
        pixmap = QPixmap(fileName)
        pixmap_resized = pixmap.scaled(400, 500, Qt.KeepAspectRatio)
        self.immage_original.setPixmap(pixmap_resized)
        #self.resize(pixmap.width(),pixmap.height())
        self.immage_original.move(50,300)
        self.immage_original.show()
        return(fileName)
    
    @pyqtSlot()
    def on_click_d_f(self):
        if(not(self.first_original)):
           self.textboxValue_f = int(self.textbox_f.text())
           self.textboxValue_d = int(self.textbox_d.text())

           image = misc.imread(self.file_path, flatten = 0)
           if (image.ndim >= 3):
               image = image[:,:,0]
           immage_compress = self.dct_compression(image, self.textboxValue_f, self.textboxValue_d)
           path_save = self.file_path + "_compress.bmp"
           misc.imsave(path_save, immage_compress)

           self.immage_compress = QLabel(self)
           pixmap = QPixmap(path_save)
           pixmap_resized = pixmap.scaled(400, 500, Qt.KeepAspectRatio)
           self.immage_compress.setPixmap(pixmap_resized)
           #self.resize(pixmap.width(),pixmap.height())
           self.immage_compress.move(500,300)
           self.immage_compress.show()
        else:
            QMessageBox.question(self, 'ERRORE', 'Caricare prima l\'immagine', QMessageBox.Ok, QMessageBox.Ok)
        


    def dct_compression(self, image, F, d):
        #compressed_image = image #copy to store the original image
        h = image.shape[0]
        #print(h)
        w = image.shape[1]
        #print(w)
        if(h%F != 0):
            h = int(h/F) * F
            #print(h)
        if(w%F != 0):
            w = int(w/F) * F
            #print(w)
        compressed_image = image[0:h, 0:w]
        #print(h)
        #print(w)
        # cycle the image in step of F
        for x in range(0,h,F):
            for y in range(0,w,F):
                cell = compressed_image[x:x+F, y:y+F]   # width of cell = F, height of cell = F
                #print("first cell:\n")
                #print(cell)
                cell = dctn(cell, type = 2, norm = 'ortho') # discrete cosine transform of the selected cell

                c_h = cell.shape[0]
                c_w = cell.shape[1]
                # delete the frequencies in the cell making reference to d parameter
                for i in range(0,c_h):
                    for j in range(0,c_w):
                        if i+j >= d:
                            cell[i,j] = 0 

                # compute the inverse dct of the cell
                cell = idctn(cell, type = 2, norm = 'ortho')

                #round of ff at the nearest integer, put to 0 negative values, put to 255 bigger values
                for i in range(0,c_h):
                    for j in range(0,c_w):
                        value = np.round(cell[i,j])
                        if value < 0:
                            value = 0
                        elif value > 255:
                            value = 255
                        cell[i,j] = value
                compressed_image[x:x+F, y:y+F] = cell

        return compressed_image


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
