class Product:
    def __init__(self, _name="", _measurements="", _price="", _barcode=""):
        self.__name = _name
        self.__measurements = _measurements
        self.__price = _price
        self.__barcode = _barcode

    def get_name(self):
        return self.__name

    def get_measurements(self):
        return self.__measurements

    def get_price(self):
        return self.__price

    def get_barcode(self):
        return self.__barcode

    def set_name(self, _name):
        self.__name = _name

    def set_measurements(self, _measurements):
        self.__measurements = _measurements

    def set_price(self, _price):
        self.__price = _price

    def set_barcode(self, _barcode):
        self.__barcode = _barcode

    def __str__(self):
        return f'{self.__name:5s}, {self.__measurements:20s}${self.__price:3.2f}'
