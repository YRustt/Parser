import os
import sys
import logging

from functools import partial


logging.basicConfig(level=logging.DEBUG)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.dirname(BASE_DIR)

DRIVERS_DIR = os.path.join(ROOT_DIR, "drivers")
if sys.platform.startswith("win"):
    CHROMEDRIVER_PATH = os.path.join(DRIVERS_DIR, "chromedriver.exe")
    GECKODRIVER_PATH = os.path.join(DRIVERS_DIR, "geckodriver.exe")
    IEDRIVER_PATH = os.path.join(DRIVERS_DIR, "iedriver.exe")
elif sys.platform.startswith("linux"):
    CHROMEDRIVER_PATH = os.path.join(DRIVERS_DIR, "chromedriver")
    GECKODRIVER_PATH = None
    IEDRIVER_PATH = None

FILES_DIR = os.path.join(ROOT_DIR, "files")
CATEGORIES_PATH = os.path.join(FILES_DIR, "categories.csv")


def __get_or_create_directory(category_name, subcategory_name):
    subcategory_dir = os.path.join(FILES_DIR, category_name, subcategory_name)
    if not os.path.exists(subcategory_dir):
        os.makedirs(subcategory_dir)
    
    return subcategory_dir


def get_filepath(category_name, subcategory_name, filename):
    subcategory_dir = __get_or_create_directory(category_name, subcategory_name)
    return os.path.join(subcategory_dir, filename)


get_product_urls_filepath = partial(get_filepath, filename="urls.csv")
get_products_filepath = partial(get_filepath, filename="products.csv")
get_products_from_category_detail_filepath = partial(get_filepath, filename="products_from_category_detail.csv")

SLEEP_TIME_FOR_LOGIN = 60 * 2
SLEEP_TIME_FOR_NEXT_PAGE = 5
SLEEP_TIME_FOR_PAGE_SCROLLING = 1
