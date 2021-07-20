import sys
import os

from PyQt6 import Qt
from PyQt6 import QtWidgets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep

import AppUI
from infogetter import InfoGetter


class GrabberApp(QtWidgets.QMainWindow, AppUI.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.grab_data)

    def grab_data(self):
        city = self.textEdit_city.toPlainText()
        type = self.textEdit_type.toPlainText()

        driver = webdriver.Safari()
        driver.maximize_window()
        driver.get('https://yandex.ru/maps')
        driver.find_element_by_class_name(name='search-form-view__input').send_keys(city + ' ' + type)
        driver.find_element_by_class_name(name='small-search-form-view__button').click()
        sleep(1)
        try:
            for i in range(1, 26):
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[9]/div/div[1]/div[1]/div[1]/div/div['
                                             f'1]/div/div/ul/div[{i}]').click()
                sleep(1)
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[10]/div/div[1]/div[1]/div[1]/div/div['
                                             '1]/div/div/div[2]/div[2]/div[2]/h1/div[1]/a').click()
                sleep(1)
                soup = BeautifulSoup(driver.page_source, "lxml")
                name = InfoGetter.get_name(soup)
                address = InfoGetter.get_address(soup)
                website = InfoGetter.get_website(soup)
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[17]/div/div/div[1]/div[1]/div[1]/div/div['
                                             '1]/div[3]/div/div/div[12]/div/div[3]/div/div/div/div[7]/div[6]/div['
                                             '2]/div/div/div[1]/div[1]/div[2]') .click()
                sleep(1)
                print(name, address, website)
                driver.back()
                driver.back()

        except:
            pass

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
