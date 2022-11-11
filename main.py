import sys

from PIL import Image
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

import funcs

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class JapaneseTranslator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)  # Загружаем дизайн
        self.file_name = ''
        self.translateButton.clicked.connect(self.translate)
        self.fileButton.clicked.connect(self.image_choose)

    def image_choose(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.prepared_image = Image.open(self.file_name).convert("RGBA")
        width, height = self.prepared_image.size
        im = self.prepared_image
        data = im.tobytes("raw", "RGBA")
        pixmap = QPixmap().fromImage(QImage(data, width, height, QImage.Format_RGBA8888))
        self.image.setPixmap(pixmap)

    def translate(self):
        chosen_language = funcs.lang_dict[self.languageBox.currentText()]
        self.japaneseText.setText('')
        self.pronunciationText.setText('')
        self.translatedText.setText('')

        if self.file_name:
            res = funcs.translate(image_path=self.file_name,
                                  lang=chosen_language)
            self.japaneseText.setText(res[0])
            self.translatedText.setText(res[2])
            if self.pronunciationCheckBox.isChecked():
                self.pronunciationText.setText(res[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JapaneseTranslator()
    ex.show()
    sys.exit(app.exec_())
