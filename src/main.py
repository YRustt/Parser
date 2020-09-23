import csv

from parsers import (
    CategoryParser, 
    CategoryDetailParser, 
    ProductParser, 
    ProductFromCategoryDetailParser
)
from writers import CSVWriter
from models import Category, Product, Url

from settings import (
    CATEGORIES_PATH, 
    get_product_urls_filepath, 
    get_products_filepath,
    get_products_from_category_detail_filepath
)


if __name__ == "__main__":
    # # Парсинг категорий
    # parser = CategoryParser("https://aliexpress.ru/all-wholesale-products.html")
    #
    # with CSVWriter(CATEGORIES_PATH, Category) as writer:
    #     writer.writerows(parser.parse())


    # # Парсинг урлов продуктов для категорий
    # with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
    #     reader = csv.DictReader(f, delimiter="\t")
    #     for i in range(36):
    #         print(next(reader))

    #     for category in reader:
    #         category = Category(**category)
    #         category_parser = CategoryDetailParser(category)
    #         filename = get_product_urls_filepath(category.category_name, category.subcategory_name)
    #         with CSVWriter(filename, Url) as writer:
    #             writer.writerows(category_parser.parse())


    # # Парсинг продуктов (урлы берутся из скачанных файлов)
    # with open(CATEGORIES_PATH, "r") as f:
    #     reader = csv.DictReader(f, delimiter="\t")
    
    #     for category in reader:
    #         urls_filename = get_product_urls_filepath(category["category_name"], category["subcategory_name"])
    #         filename = get_products_filepath(category["category_name"], category["subcategory_name"])
    #         with open(urls_filename, "r") as f2, CSVWriter(filename, Product) as writer:
    #             reader2 = csv.DictReader(f2, delimiter="\t")
    
    #             for url in reader2:
    #                 url = Url(**url)
    #                 product_parser = ProductParser(url)
    #                 writer.writerow(product_parser.parse())


    # # Парсинг продуктов (урлы парсятся и сохраняются одновременно)
    # with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
    #     reader = csv.DictReader(f, delimiter="\t")
    
    #     for category in reader:
    #         if category["category_name"] in ["Мобильные телефоны и аксессуары", "Компьютерная и офисная техника"]:
    #             category = Category(**category)
    #             category_parser = CategoryDetailParser(category)
    #             urls_filename = get_product_urls_filepath(category.category_name, category.subcategory_name)
    #             filename = get_products_filepath(category.category_name, category.subcategory_name)
    #             with CSVWriter(urls_filename, Url) as url_writer, CSVWriter(filename, Product) as writer:
    #                 for url in category_parser.parse():
    #                     url_writer.writerow(url)
    #                     product_parser = ProductParser(url)
    #                     writer.writerow(product_parser.parse())


    # Парсинг продуктов со страниц категории (урлы сохраняются в файл с продуктами)
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
    
        for category in reader:
            if category["category_name"] in ["Компьютерная и офисная техника"]:
                category = Category(**category)
                product_parser = ProductFromCategoryDetailParser(category)
                filename = get_products_from_category_detail_filepath(category.category_name, category.subcategory_name)
                with CSVWriter(filename, Product) as writer:
                    for product in product_parser.parse():
                        writer.writerow(product)
