from SupermarketDAO import SupermarketDAO
from Transaction import Transaction
from Product import Product
import sqlite3
from datetime import datetime
import random as rng
import UI


def main():
    UI.start()
    # dao = SupermarketDAO("checkout.db")
    # for i in range(10):
    #     dao.addProductToDB(Product(("10" + str(i)), ("dummy" + str(i)), "dummy product", (i + 1) * 1.12))
    # for i in range(4):
    #     for j in range(10):
    #         dao.addTransactionToDB(Transaction(datetime.now().strftime("%Y-%m-%d  %H:%M:%S.%f")[:-3], rng.randint(100, 109), ((j + 1) * 1.12) * rng.randint(1, i + 1)))


main()
