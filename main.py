import sys
import os

from PyQt6 import Qt
from PyQt6 import QtWidgets
from selenium import webdriver
from time import sleep

import AppUI


OUT_FILE = "./OUTPUT.txt"


def output_data(data):
    f = open(OUT_FILE, 'a')
    f.write(data)
    f.close()


class GrabberApp(QtWidgets.QMainWindow, AppUI.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.grab_data)

    def grab_data(self):
        city = self.textEdit_city.toPlainText()
        type = self.textEdit_type.toPlainText()

        driver = webdriver.Safari()
        driver.get('https://yandex.ru/maps')
        driver.find_element_by_class_name(name='search-form-view__input').send_keys(city + ' ' + type)
        sleep(1)
        driver.find_element_by_class_name(name='small-search-form-view__button').click()
        sleep(5)
        driver.quit()

        self.label.setText('Данные сохранены')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GrabberApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
