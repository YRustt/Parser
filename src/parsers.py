import logging
import requests

from abc import ABCMeta, abstractmethod
from urllib.parse import urlencode
from lxml import html

from browsers import ChromeBrowser, FirefoxBrowser, IeBrowser
from models import Category, Product, Url


logger = logging.getLogger(__name__)


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self):
        pass


class GetPageMixin:
    def _get_url(self):
        raise NotImplementedError()

    def _get_page(self):
        response = requests.get(self._get_url())

        # TODO: Error code handling
        if response.status_code == 200:
            return response.text


class GetPageViaBrowserMixin:
    def _get_url(self):
        raise NotImplementedError()

    def _get_page(self):
        browser = ChromeBrowser()
        page = browser.get_page(self._get_url())
        return page


class CategoryParser(Parser, GetPageMixin):
    CATEGORY_XPATH = "//div[@class='cg-main']/div[@class='item util-clearfix']"
    CATEGORY_NAME_XPATH = ".//h3/a/text()"
    SUBCATEGORY_XPATH = ".//div[@class='sub-item-wrapper util-clearfix']/div[@class='sub-item-cont-wrapper']/ul/li/a"
    SUBCATEGORY_NAME_XPATH = ".//text()"
    URL_XPATH = ".//@href"

    def __init__(self, url):
        self.__url = url

    def _get_url(self):
        return self.__url

    def parse(self):
        text = self._get_page()
        tree = html.fromstring(text)
        for category_tree in tree.xpath(self.CATEGORY_XPATH):
            category_name = category_tree.xpath(self.CATEGORY_NAME_XPATH)[0]
            for subcategory_tree in category_tree.xpath(self.SUBCATEGORY_XPATH):
                subcategory_name = subcategory_tree.xpath(self.SUBCATEGORY_NAME_XPATH)[0]
                url = subcategory_tree.xpath(self.URL_XPATH)[0]

                category = Category(category_name, subcategory_name, url)
                logger.debug(category)

                yield category


class CategoryDetailParser(Parser, GetPageViaBrowserMixin):
    PRODUCT_URL_XPATH = "//div[@class='gallery-wrap product-list']/ul/div/li[@class='list-item']/div/div/div/a/@href"

    def __init__(self, category):
        self.__category = category
        self.__page = 1

    def _get_url(self):
        get_args = urlencode({"page": self.__page})
        self.__page += 1

        if self.__category.url.startswith("http"):
            return f"{self.__category.url}?{get_args}"
        elif self.__category.url.startswith("//"):
            return f"https:{self.__category.url}?{get_args}"
        else:
            return f"https://{self.__category.url}?{get_args}"

    def parse(self):
        while True:
            text = self._get_page()
            tree = html.fromstring(text)

            urls = tree.xpath(self.PRODUCT_URL_XPATH)

            if not urls:
                break

            for idx, url in enumerate(urls):
                logger.debug(f"{self.__page} {idx} {url}")

            yield from (Url(url) for url in urls)


class ProductParser(Parser, GetPageMixin):
    def __init__(self, url):
        self.__url = url
