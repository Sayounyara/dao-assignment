class Transaction:
    def __init__(self, _date="1970-01-01  00:00:00.000", _barcode="", _amount=0.0):
        #                     YYYY-MM-DD  HH:MM:SS.SSS
        self.__date = _date
        self.__barcode = _barcode
        self.__amount = _amount

    def get_date(self):
        return self.__date

    def get_barcode(self):
        return self.__barcode

    def get_amount(self):
        return self.__amount

    def __str__(self):
        return f'{self.__date} > ({self.__barcode}) : ${self.__amount:3.2f}'
