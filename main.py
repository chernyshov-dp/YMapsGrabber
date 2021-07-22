import sys

from PyQt6 import QtWidgets
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
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
        '''
        chrome_options = webdriver.ChromeOptions
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1420,1080")  <- Настройки для хрома
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        '''

        # Создаем OUTPUT.json
        util_module.JSONWorker("get", "")

        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Safari()
        driver.maximize_window()
        driver.get('https://yandex.ru/maps')

        # Вводим данные поиска
        driver.find_element_by_class_name(name='search-form-view__input').send_keys(city + ' ' + type)

        # Нажимаем на кнопку поиска
        driver.find_element_by_class_name(name='small-search-form-view__button').click()
        sleep(2)

        slider = driver.find_element_by_class_name(name='scroll__scrollbar-thumb')
        # Основная вкладка со списком всех организаций
        parent_handle = driver.window_handles[0]

        id = 0
        organizations_href = ""
        try:
            for i in range(250):
                ActionChains(driver).click_and_hold(slider).move_by_offset(0, 100).release().perform()

                # Нажимаем на организацию в общем поиске
                if (id == 0) or (id % 5 == 0):
                    organizations_href = driver.find_elements_by_class_name(name='search-snippet-view__link-overlay')
                organization_url = organizations_href[i].get_attribute("href")

                # Открываем карточку организации в новой вкладке
                driver.execute_script(f'window.open("{organization_url}","org_tab");')
                child_handle = [x for x in driver.window_handles if x != parent_handle][0]
                driver.switch_to.window(child_handle)
                sleep(1)

                soup = BeautifulSoup(driver.page_source, "lxml")
                id += 1
                name = InfoGetter.get_name(soup)
                address = InfoGetter.get_address(soup)
                website = InfoGetter.get_website(soup)
                opening_hours = InfoGetter.get_opening_hours(soup)
                ypage = driver.current_url
                rating = InfoGetter.get_rating(soup)

                # Формирование ссылки на отзывы
                current_url_split = ypage.split('/')

                goods = ""
                try:
                    menu = driver.find_element_by_class_name(name='card-feature-view__main-content')
                    menu_text = driver.find_element_by_class_name(name='card-feature-view__main-content').text

                    if ('товары и услуги' in menu_text.lower()) or ('меню' in menu_text.lower()):
                        # Нажимаем на кнопку "Меню"/"Товары и услуги"
                        menu.click()
                        sleep(2)
                        soup = BeautifulSoup(driver.page_source, "lxml")
                        goods = InfoGetter.get_goods(soup)
                except NoSuchElementException:
                    pass

                #  Переходим на вкладку "Отзывы"
                reviews_url = 'https://yandex.ru/maps/org/' + current_url_split[5] + '/' + current_url_split[6] + \
                              '/reviews'
                driver.get(reviews_url)
                sleep(2)

                reviews = InfoGetter.get_reviews(soup, driver)

                # Записываем данные в OUTPUT.json
                output = json_pattern.into_json(id, name, address, website, opening_hours, ypage, goods, rating,
                                                reviews)
                util_module.JSONWorker("set", output)

                driver.close()
                driver.switch_to.window(parent_handle)
                sleep(1)

        except:
            pass

        self.label.setText('Данные сохранены в OUTPUT.json')
        driver.quit()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = GrabberApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
