import csv


class CSVWriter:
    def __init__(self, filename, model):
        self.__filename = filename
        self.__model = model
        self.__file = None
        self.__writer = None

    def __enter__(self):
        return self

    def __exit__(self, ext_type, ext_val, ext_tb):
        self.__clear()

    def __setup(self):
        if self.__file is None:
            self.__file = open(self.__filename, "w", newline="", encoding="utf-8")
            self.__writer = csv.DictWriter(self.__file, fieldnames=self.__model.field_names(), delimiter="\t")
            self.__writer.writeheader()

    def __clear(self):
        if self.__file is not None:
            self.__file.close()

    def writerows(self, items):
        self.__setup()
        self.__writer.writerows(item.as_dict() for item in items)

    def writerow(self, item):
        self.__setup()
        self.__writer.writerow(item.as_dict())


class DBWriter:
    pass
