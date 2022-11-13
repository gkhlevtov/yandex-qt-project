import sys

from PIL import Image, ImageEnhance
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
        self.contrast = 1
        self.brightness = 1
        self.sharpness = 1

        self.translateButton.clicked.connect(self.translate)
        self.fileButton.clicked.connect(self.image_choose)

        self.contrastUpButton.clicked.connect(self.contrast_up)
        self.contrastDownButton.clicked.connect(self.contrast_down)

        self.brightnessUpButton.clicked.connect(self.brightness_up)
        self.brightnessDownButton.clicked.connect(self.brightness_down)

        self.sharpnessUpButton.clicked.connect(self.sharpness_up)
        self.sharpnessDownButton.clicked.connect(self.sharpness_down)

    def image_choose(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        img = Image.open(self.file_name).convert("RGBA")

        self.prepared_image = img
        self.original_image = img

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
            res = funcs.translate(image=self.prepared_image,
                                  lang=chosen_language)
            self.japaneseText.setText(res[0])
            self.translatedText.setText(res[2])
            if self.pronunciationCheckBox.isChecked():
                self.pronunciationText.setText(res[1])

    def image_enhance(self):

        width, height = self.prepared_image.size

        contrast_enhancer = ImageEnhance.Contrast(self.original_image)
        im_output = contrast_enhancer.enhance(self.contrast)

        brightness_enhancer = ImageEnhance.Brightness(im_output)
        im_output = brightness_enhancer.enhance(self.brightness)

        sharpness_enhancer = ImageEnhance.Sharpness(im_output)
        im_output = sharpness_enhancer.enhance(self.sharpness)

        self.prepared_image = im_output
        data = self.prepared_image.tobytes("raw", "RGBA")
        pixmap = QPixmap().fromImage(QImage(data, width, height, QImage.Format_RGBA8888))
        self.image.setPixmap(pixmap)

    def contrast_up(self):
        self.contrast += 0.25
        self.image_enhance()

    def contrast_down(self):
        self.contrast -= 0.25
        self.image_enhance()

    def brightness_up(self):
        self.brightness += 0.5
        self.image_enhance()

    def brightness_down(self):
        self.brightness -= 0.5
        self.image_enhance()

    def sharpness_up(self):
        self.sharpness += 0.1
        self.image_enhance()

    def sharpness_down(self):
        self.sharpness -= 0.1
        self.image_enhance()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JapaneseTranslator()
    ex.show()
    sys.exit(app.exec_())
