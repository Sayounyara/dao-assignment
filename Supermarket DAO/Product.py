class Product:
    def __init__(self, barcode="", _name="", _desc="", _price=0.0):
        self.__barcode = barcode
        self.__name = _name
        self.__desc = _desc
        self.__price = _price

    def get_barcode(self):
        return self.__barcode

    def get_name(self):
        return self.__name

    def get_desc(self):
        return self.__desc

    def get_price(self):
        return self.__price

    def set_barcode(self, _barcode):
        self.__barcode = _barcode

    def set_name(self, _name):
        self.__name = _name

    def set_desc(self, _desc):
        self.__desc = _desc

    def set_price(self, _price):
        self.__price = _price

    def __str__(self):
        return f'{self.__name:5s}: {self.__desc}\n${self.__price:3.2f}'
