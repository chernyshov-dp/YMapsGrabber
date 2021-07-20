import os
import re
import time


OUT_FILE = "./OUTPUT.txt"


def output_data(data):
    f = open(OUT_FILE, 'a')
    f.write(data)
    f.close()


class InfoGetter(object):

    @staticmethod
    def get_name(soup_content):
        try:
            for data in soup_content.find_all(
                    "h1", {"class": "orgpage-header-view__header"}
            ):
                name = data.getText()

            return name
        except:
            return ""

    @staticmethod
    def get_address(soup_content):
        try:
            for data in soup_content.find_all(
                    "div", {"class": "business-contacts-view__address-link"}
            ):
                address = data.getText()

            return address
        except:
            return ""

    @staticmethod
    def get_website(soup_content):
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
        opening_hours = []
        try:
            for data in soup_content.find_all(
                    "meta", {"itemprop": "openingHours"}
            ):
                opening_hours.append(data.get('content'))

            return opening_hours
        except:
            return ""

    @staticmethod
    def get_goods(soup_content):
        pass

    @staticmethod
    def get_reviews(soup_content):
        pass
