import csv

from parsers import CategoryParser, CategoryDetailParser, ProductParser
from writers import CSVWriter
from models import Category, Product, Url

from settings import CATEGORIES_PATH, get_product_urls_filepath, get_products_filepath


if __name__ == "__main__":
    # parser = CategoryParser("https://aliexpress.ru/all-wholesale-products.html")
    #
    # with CSVWriter(CATEGORIES_PATH, Category) as writer:
    #     writer.writerows(parser.parse())


    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for i in range(36):
            print(next(reader))

        # for category in reader:
        #     category = Category(**category)
        #     category_parser = CategoryDetailParser(category)
        #     filename = get_product_urls_filepath(category.category_name, category.subcategory_name)
        #     with CSVWriter(filename, Url) as writer:
        #         writer.writerows(category_parser.parse())


    # with open(CATEGORIES_PATH, "r") as f:
    #     reader = csv.DictReader(f, delimiter="\t")
    #
    #     for category in reader:
    #         urls_filename = get_product_urls_filepath(category["category_name"], category["subcategory_name"])
    #         filename = get_products_filepath(category["category_name"], category["subcategory_name"])
    #         with open(urls_filename, "r") as f2, CSVWriter(filename, Product) as writer:
    #             reader2 = csv.DictReader(f2, delimiter="\t")
    #
    #             for url in reader2:
    #                 url = Url(**url)
    #                 product_parser = ProductParser(url)
    #                 writer.writerow(product_parser.parse())
