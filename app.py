#!/usr/local/bin/python3
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QGridLayout, QGroupBox, QPushButton, QRadioButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QMessageBox
import os
import predict, test_preprocessing, train

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.title = 'Программа'
        self.initUI()
        self.resize(300, 100)

    def initUI(self):
        grid = QGridLayout()

        groupBox = QGroupBox('Путь к папке с документами:')
        grid1 = QGridLayout()
        self.pDir = QLineEdit()
        self.pDir.setReadOnly(True)
        pDirButton = QPushButton('...')
        pDirButton.clicked.connect(self.pButton_click)

        grid1.addWidget(self.pDir, 0, 0)
        grid1.addWidget(pDirButton, 0, 1)
        groupBox.setLayout(grid1)

        buttonModel = QPushButton('Произвести разметку')
        buttonModel.clicked.connect(self.applyModel)

        self.buttonSend = QPushButton('Отправить на ручную разметку')
        self.buttonSend.setEnabled(False)
        self.buttonSend.clicked.connect(self.toIndexStation)

        grid.addWidget(groupBox, 0, 0)
        grid.addWidget(buttonModel, 1, 0)
        grid.addWidget(self.buttonSend, 2, 0)

        self.setLayout(grid)
        self.setWindowTitle(self.title)

    def toIndexStation(self):
        self.showMessageBox('Сообщение', 'Успешно!\n' + 'Документы отправлены на ручную разметку.')
    
    def applyModel(self):
        m = train.Seq2SeqModel()
        input_token_dict, output_token_dict = m.model_load('./model/')
        encoder_model, decoder_model = m.encdec()
        p = predict.Predict(encoder_model, decoder_model, input_token_dict, output_token_dict)
        self.d1, self.d0 = p.predict(self.path)
        self.showMessageBox('Сообщение', 'Успешно!\n' + 'Результаты сохранены.')
        self.buttonSend.setEnabled(True)
        

    def showMessageBox(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        button = msg.addButton('ОК', QMessageBox.AcceptRole)
        msg.exec_()
        msg.deleteLater()

    def pButton_click(self):
        name = QFileDialog.getExistingDirectory(self, 'Select Input Folder"', './')
        if name:
            self.path = name
            self.pDir.setText(name)

if __name__ == '__main__':
    import sys
    QApplication.setStyle("fusion") #here
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
