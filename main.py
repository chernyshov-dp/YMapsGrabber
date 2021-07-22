import sys
import os

from PyQt6 import Qt
from PyQt6 import QtWidgets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep


import AppUI
import json_pattern
import util_module
from infogetter import InfoGetter


class GrabberApp(QtWidgets.QMainWindow, AppUI.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.grab_data)

    def grab_data(self):
        city = self.textEdit_city.toPlainText()
        type = self.textEdit_type.toPlainText()
        util_module.JSONWorker("get", "")

        driver = webdriver.Safari()
        driver.maximize_window()
        driver.get('https://yandex.ru/maps')

        # Вводим данные поиска
        driver.find_element_by_class_name(name='search-form-view__input').send_keys(city + ' ' + type)

        # Нажимаем на кнопку поиска
        driver.find_element_by_class_name(name='small-search-form-view__button').click()
        sleep(2)
        id = 0
        try:
            for i in range(1, 26):

                # Нажимаем на организацию в общем поиске
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[9]/div/div[1]/div[1]/div[1]/div/div['
                                             f'1]/div/div/ul/div[{i}]').click()
                sleep(1)

                # Нажимаем на карточку организации
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[10]/div/div[1]/div[1]/div[1]/div/div['
                                             '1]/div/div/div[2]/div[2]/div[2]/h1/div[1]/a').click()
                sleep(1)

                soup = BeautifulSoup(driver.page_source, "lxml")
                id += 1
                name = InfoGetter.get_name(soup)
                address = InfoGetter.get_address(soup)
                website = InfoGetter.get_website(soup)
                opening_hours = InfoGetter.get_opening_hours(soup)
                ypage = driver.current_url
                rating = InfoGetter.get_rating(soup)

                menu = driver.find_element_by_class_name(name='card-feature-view__main-content')
                menu_text = driver.find_element_by_class_name(name='card-feature-view__main-content').text
                goods = ""
                if ('товары и услуги' in menu_text.lower()) or ('меню' in menu_text.lower()):
                    # Нажимаем на кнопку "Меню"/"Товары и услуги"
                    menu.click()
                    sleep(1)
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    goods = InfoGetter.get_goods(soup)

                #  Нажимаем на кнопку "Отзывы"
                #driver.find_element_by_xpath('').click
                sleep(1)

                # reviews = InfoGetter.get_reviews(soup)

                # Записываем данные в
                output = json_pattern.into_json(id, name, address, website, opening_hours, ypage, goods, rating, 'reviews')
                util_module.JSONWorker("set", output)

                print(
                    json_pattern.into_json(id, name, address, website, opening_hours, ypage, goods, rating, 'reviews'))
                driver.back()
                driver.back()

        except:
            pass

        driver.quit()

        self.label.setText('Данные сохранены в OUTPUT.json')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GrabberApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
