import settings
from parsers import CategoryParser, CategoryDetailParser
from writers import CSVWriter
from models import Category, Product, Url

from settings import CATEGORIES_PATH, get_product_urls_filepath, get_products_filepath


if __name__ == "__main__":
    parser = CategoryParser("https://aliexpress.ru/all-wholesale-products.html")

    # with CSVWriter(CATEGORIES_PATH, Category) as writer:
    #     writer.write(parser.parse())

    for category in parser.parse():
        category_parser = CategoryDetailParser(category)
        filename = get_product_urls_filepath(category.category_name, category.subcategory_name)
        with CSVWriter(filename, Url) as writer:
            items = list(category_parser.parse())
            print(items)
            writer.write(items)
