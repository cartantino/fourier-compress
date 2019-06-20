import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Metodi del calcolo Scientifico'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.button = QPushButton('Carica', self)
        self.button.setToolTip('Carica')
        self.button.move(300,70)
        self.file_path = None
        self.button.clicked.connect(self.on_click_carica)
        
        # Create textox for f
        self.textbox_f = QLineEdit(self)
        self.textbox_f.move(20, 100)
        self.textbox_f.resize(100,40)

        # Create textbox for d
        self.textbox_d = QLineEdit(self)
        self.textbox_d.move(20, 150)
        self.textbox_d.resize(100,40)

        # connect button to function on_click_d_f
        # Create a button in the window
        self.button_d_f = QPushButton('Esegui', self)
        self.button_d_f.move(200,150)
        self.button_d_f.clicked.connect(self.on_click_d_f)
        self.show()

        #self.saveFileDialog()
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Open", "","bmp Files (*.bmp);;All Files (*)", options=options)
        return(fileName)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    @pyqtSlot()
    def on_click_carica(self):
        fileName = self.openFileNameDialog()
        #self.file_path = fileName
        self = QLabel(self)
        pixmap = QPixmap(fileName)
        self.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        #self.show()

    
    @pyqtSlot()
    def on_click_d_f(self):
        textboxValue_f = self.textbox_f.text()
        textboxValue_d = self.textbox_d.text()
        print(textboxValue_f)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
