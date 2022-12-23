import sqlite3

from Product import Product
import datetime

# This opens the product.txt file and breaks the file down into
# something the program can read, then it adds it to a list. It
# then returns the list.
def load(db_name):
    l = list()
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS products(barcode TEXT(10), name TEXT(10), desc TEXT(255), price REAL(5,2));")
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions(date TEXT(24), barcode TEXT(10), amount REAL(5,2));")
    cursor.execute("SELECT * FROM products;")
    for i in cursor:
        l.append(Product(i[1], i[2], i[3], i[0]))
    db.commit()
    db.close()
    return l


class CheckoutRegister:
    # The __init__ function initializes the object with a product
    # list loaded from a file, an empty receipt, and three floats
    # to be filled out as the customer continues with their order.
    def __init__(self):
        self.__database_name = 'checkout.db'
        self.__product_list = load(self.__database_name)
        self.__receipt = list()
        self.__total = 0.0
        self.__paid = 0.0
        self.__balance = 0.0

    # This checks the given barcode and checks it within the product
    # list. If it is there, it adds the product to the receipt list,
    # adds the products price to the total, and saves the transaction
    # to the transaction.txt file. If it cannot find it, it raises
    # an IndexError.
    def scan_item(self, product_barcode):
        for i in self.__product_list:
            if i.get_barcode() == product_barcode:
                self.__receipt.append(i)
                self.__total += i.get_price()
                self.save_transaction(datetime.datetime.now(), product_barcode, i.get_price())
                return

        raise IndexError("Couldn't find barcode.")

    # This checks if the amount_paid variable is only numbers first.from
    # If not, it raises a TypeError Exception. Then, it checks to see if
    # amount_paid is negative, to which it raises a ValueError. If it
    # passes these tests it gets added to the paid amount. If the paid
    # amount is bigger than the total, it returns True, else it returns
    # False.
    def accept_payment(self, amount_paid):
        if amount_paid.isalpha():
            raise TypeError("amount paid cannot contain alphabetical characters.")
        amount_paid = float(amount_paid)
        if amount_paid < 0:
            raise ValueError("Amount paid cannot be negative.")

        self.__paid += amount_paid
        if self.__paid >= self.__total:
            return True
        else:
            return False

    # Returns the payment due.
    def get_due(self):
        return self.__total - self.__paid

    # This prints the receipt list, and the total, amount received, and
    # balance given.
    def print_receipt(self):
        print("----- Final Receipt -----")
        print()
        self.__balance = self.__paid - self.__total
        for i in self.__receipt:
            print(i)

        print()
        print(f'Total amount due: ${self.__total:3.2f}')
        print(f'Amount received:  ${self.__paid:3.2f}')
        print(f'Balance given:    ${self.__balance:3.2f}')

    # Saves the time, and barcode and price of the product to the
    # transactions.txt file
    def save_transaction(self, date, barcode, amount):
        db = sqlite3.connect(self.__database_name)
        cursor = db.cursor()
        cursor.execute('''INSERT INTO transactions VALUES (?, ?, ?);''', (date, barcode, amount, ))
        db.commit()
        db.close()
