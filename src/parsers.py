import logging
import requests

from abc import ABCMeta, abstractmethod
from lxml import html

from utils import make_url, get_product_id_from_url
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
        self.__repeat = 0

    def _get_url(self):
        return make_url(self.__category.url, page=self.__page)

    def _next_page(self):
        self.__page += 1
        self.__repeat = 0

    def _check_repeat(self):
        return self.__repeat < 5

    def _next_repeat(self):
        self.__repeat += 1

    def parse(self):
        while True:
            text = self._get_page()
            tree = html.fromstring(text)

            urls = tree.xpath(self.PRODUCT_URL_XPATH)

            if not urls:
                if self._check_repeat():
                    self._next_repeat()
                    continue
                break

            for idx, url in enumerate(urls):
                logger.debug(f"{self.__page} {idx} {url}")

            yield from (Url(url) for url in urls)

            self._next_page()


class ProductParser(Parser, GetPageViaBrowserMixin):
    DESCRIPTION_XPATH = "//div[@class='product-title']/h1[@class='product-title-text']/text()"
    NUMBER_OF_ORDERS_XPATH = "//div[@class='product-reviewer']/span[@class='product-reviewer-sold']/text()"
    PRICE_XPATH = "//div[@class='product-price']/div[@class='product-price-current']/span[@class='product-price-value']/text()"

    def __init__(self, url):
        self.__url = url

    def _get_url(self):
        return make_url(self.__url.url, g="y")

    def __get_id_from_url(self):
        url = self._get_url()
        return get_product_id_from_url(url)

    def parse(self):
        text = self._get_page()
        tree = html.fromstring(text)

        id = self.__get_id_from_url()

        description = tree.xpath(self.DESCRIPTION_XPATH)[0]

        tmp = tree.xpath(self.NUMBER_OF_ORDERS_XPATH)
        number_of_orders = tmp[0] if tmp else None

        tmp = tree.xpath(self.PRICE_XPATH)
        price = tmp[0] if tmp else None

        url = self.__url.url

        product = Product(id=id, description=description, number_of_orders=number_of_orders, price=price, url=url)

        logger.debug(product)

        return product


class ProductFromCategoryDetailParser(Parser, GetPageViaBrowserMixin):
    PRODUCT_XPATH = "//ul[@class='list-items']/div/li[@class='list-item']"
    DESCRIPTION_XPATH = ".//div[@class='hover-help']/div[@class='item-title-wrap']/a/text()"
    NUMBER_OF_ORDERS_XPATH = ".//div[@class='item-sale-wrap']/div[@class='sale-info with-star']/span[@class='sale-value']/a/text()"
    PRICE_XPATH = ".//div[@class='item-price-wrap']/div/span[@class='price-current']/text()"
    URL_XPATH = ".//div[@class='product-img']/div[@class='place-container']/a/@href"

    def __init__(self, category):
        self.__category = category
        self.__page = 1
        self.__repeat = 0

    def _get_url(self):
        return make_url(self.__category.url, page=self.__page, g="y")

    def _next_page(self):
        self.__page += 1
        self.__repeat = 0

    def _check_repeat(self):
        return self.__repeat < 5

    def _next_repeat(self):
        self.__repeat += 1

    def _check_limit(self):
        return self.__page < 70

    def parse(self):
        while True:
            if not self._check_limit():
                break

            text = self._get_page()
            tree = html.fromstring(text)

            products_tree = tree.xpath(self.PRODUCT_XPATH)

            if not products_tree:
                if self._check_repeat():
                    self._next_repeat()
                    continue
                break

            for idx, product_tree in enumerate(products_tree):
                description = product_tree.xpath(self.DESCRIPTION_XPATH)[0]

                tmp = product_tree.xpath(self.NUMBER_OF_ORDERS_XPATH)
                number_of_orders = tmp[0] if tmp else None
                
                tmp = product_tree.xpath(self.PRICE_XPATH)
                price = tmp[0] if tmp else None
                
                url = product_tree.xpath(self.URL_XPATH)[0]

                id = get_product_id_from_url(url)

                product = Product(id=id, description=description, number_of_orders=number_of_orders, price=price, url=url)

                logger.debug(f"{self.__page} {idx} {product}")

                yield product

            self._next_page()
