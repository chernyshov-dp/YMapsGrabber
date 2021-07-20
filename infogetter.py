import os
import re
import time

from selenium.common.exceptions import NoSuchElementException

OUT_FILE = "./OUTPUT.txt"


def output_data(data):
    f = open(OUT_FILE, 'a')
    f.write(data)
    f.close()


class InfoGetter(object):
    """ Класс с логикой парсинга данных из объекта BeautifulSoup"""

    @staticmethod
    def get_name(soup_content):
        """ Получение названия организации """

        try:
            for data in soup_content.find_all("h1", {"class": "orgpage-header-view__header"}):
                name = data.getText()

            return name
        except:
            return ""

    @staticmethod
    def get_address(soup_content):
        """ Получение адреса организации """

        try:
            for data in soup_content.find_all("div", {"class": "business-contacts-view__address-link"}):
                address = data.getText()

            return address
        except:
            return ""

    @staticmethod
    def get_website(soup_content):
        """ Получение сайта организации"""

        try:
            for data in soup_content.find_all(
                    "span", {"class": "business-urls-view__text"}
            ):
                website = data.getText()

            return website
        except:
            return ""

    @staticmethod
    def get_opening_hours(soup_content):
        """ Получение графика работы"""

        opening_hours = []
        try:
            for data in soup_content.find_all("meta", {"itemprop": "openingHours"}):
                opening_hours.append(data.get('content'))

            return opening_hours
        except:
            return ""

    @staticmethod
    def get_goods(soup_content):
        """ Получение списка товаров и услуг"""

        goods = []
        try:
            for data in soup_content.find_all("div", {"class": "related-item-list-view__title"}):
                goods.append(data.getText())

            return goods

        except NoSuchElementException:
            try:
                for data in soup_content.find_all("div", {"class": "related-item-photo-view__title"}):
                    goods.append(data.getText())
            except:
                return ""

        except:
            return ""


    @staticmethod
    def get_reviews(soup_content):
        pass
