from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtQuick import *

import sys
import os
from os import path

from PyQt5.uic import loadUiType

from src.lsb_algorithm import LSB

Form_Class, _ = loadUiType(path.join(path.dirname(__file__), "project.ui"))


class Main(QWidget, Form_Class):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        os.environ['QT_QUICK_CONTROLS_STYLE'] = 'Default'
        QWidget.__init__(self)
        self.setupUi(self)
        self.label = QLabel(self.label_3)
        self.init_ui()
        self.image_path = ''
        self.text_file = ''
        self.handel_buttons()

    def init_ui(self):
        self.setWindowTitle('Hacking Image')

        self.label.setScaledContents(True)

    def handel_buttons(self):
        self.pushButton.clicked.connect(self.select_cover)
        self.pushButton_2.clicked.connect(self.select_text)
        self.pushButton_3.clicked.connect(self.hide)
        self.pushButton_4.clicked.connect(self.extract)

    def select_cover(self):
        fname = QFileDialog.getOpenFileName(self, caption='Select Image', filter="Image files (*.png )")[0]
        print(fname)
        if fname:
            self.image_path = fname
            self.lineEdit.setText(fname)
            self.label_3.setPixmap(QPixmap(fname))

    def select_text(self):
        fname = QFileDialog.getOpenFileName(self, caption='Select Text File', filter="Text file (*.txt )")[0]
        print(fname)
        if fname:
            self.text_file = fname
            self.lineEdit_2.setText(fname)

    def hide(self):
        print('hide')
        if self.text_file != '' and self.image_path != '':
            save_dir = QFileDialog.getSaveFileName(self, caption='Save File', filter="Image file (*.png )")[0]
            if save_dir:
                lsb = LSB(data_path=self.text_file, image_path=self.image_path, save_path=save_dir)
                lsb.hide_bits()

    def extract(self):
        print('extract')
        if self.image_path != '':
            save_dir = QFileDialog.getSaveFileName(self, caption='Save File', filter="Text file (*.txt )")[0]
            if save_dir:
                lsb = LSB(image_path=self.image_path, save_path=save_dir)
                lsb.extract_bits()


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
