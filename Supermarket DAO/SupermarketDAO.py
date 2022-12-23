from Product import Product
from Transaction import Transaction
import sqlite3
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

class SupermarketDAO:
    def __init__(self, _databaseName="db"):
        self.__databaseName = _databaseName
        # Connects to the checkout database
        db = sqlite3.connect(self.__databaseName)
        cursor = db.cursor()
        # Creates the database if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS products(barcode TEXT(10), name TEXT(10), desc TEXT(255), price REAL(5,2));")
        cursor.execute("CREATE TABLE IF NOT EXISTS transactions(date TEXT(24), barcode TEXT(10), amount REAL(5,2));")
        db.commit()
        db.close()

    def addProductToDB(self, product_object=Product):
        try:
            db = sqlite3.connect(self.__databaseName)
            cursor = db.cursor()
            # Takes each field of the given product object
            productBarcode = product_object.get_barcode()
            productName = product_object.get_name()
            productDesc = product_object.get_desc()
            productPrice = product_object.get_price()
            # And trys to add it to the database
            cursor.execute('''INSERT INTO products VALUES (?,?,?,?);''',
                       (productBarcode, productName, productDesc, productPrice))
            # If successful, print an appropriate message and commit the changes
            print('Product successfully added to database.')
            db.commit()
            return True
        except Exception as e:
            # If it fails, it prints an appropriate error message
            print(f'Failed to add product to database. {e}')
            return False
        finally:
            # If it passes or not, the database closes
            db.close()

    def listAllProducts(self):
        db = sqlite3.connect(self.__databaseName)
        cursor = db.cursor()
        # Selects everything from the products table
        cursor.execute("SELECT * FROM products;")
        products = list()
        for i in cursor:
            # Adds each found object to a list of Product objects
            t = Product(i[0], i[1], i[2], i[3])
            products.append(t)
        db.close()
        # If the list is empty, print an appropriate message
        if len(products) == 0:
            print("No products were found in the database.")
        else:
            # Sorts the list by barcode and returns it
            products.sort(key=lambda x: x.get_barcode())
            return products

    def findProduct(self, with_this_barcode):
        try:
            db = sqlite3.connect(self.__databaseName)
            cursor = db.cursor()
            # Selects the products that have the given barcode
            cursor.execute('SELECT * FROM products WHERE barcode=?;', (with_this_barcode,))
            product = cursor.fetchone()
            # Add the selected data to a Product object and return it
            product = Product(product[0], product[1], product[2], product[3])
            return product
        except Exception as e:
            # If an error occurs, print an appropriate message
            print(f"An error occurred. {e}")
            return None
        finally:
            # If it passes or not, the database closes
            db.close()

    def listAllTransactions(self):
        db = sqlite3.connect(self.__databaseName)
        cursor = db.cursor()
        # Select everything from the transactions table
        cursor.execute("SELECT * FROM transactions;")
        transactions = list()
        # Takes the found data and adds it to a list of Transaction objects
        for i in cursor:
            t = Transaction(i[0], i[1], i[2])
            transactions.append(t)
        db.close()
        # If the list is empty, display an appropriate message
        if len(transactions) == 0:
            print('No transactions were found.')
        else:
            # Sort by date and return the list
            transactions.sort(key=lambda x: x.get_date())
            return transactions

    def displayBarchartOfProductsSold(self):
        try:
            db = sqlite3.connect(self.__databaseName)
            cursor = db.cursor()
            # Select everything from the transactions table
            cursor.execute("SELECT * FROM transactions;")
            data = cursor.fetchall()
            print(data)
            count = dict()
            # Add it to a dictionary where the barcode is the key and how many times
            # It shows up is the value
            for i in data:
                if i[1] not in count:
                    count[i[1]] = 1
                else:
                    count[i[1]] += 1
            # Convert it to a list and add titles to the start of it
            cells = list(count.items())
            cells.insert(0, ["Barcode", "Sales Volume"])
            print(count)
            print(cells)

            # Create a workbook and sheet
            wb = Workbook()
            sheet = wb.active
            # Add data to the sheet
            for i in cells:
                sheet.append(i)
            # save it as chart1.xlsx
            wb.save("chart1.xlsx")

            # Create barchart data
            chart = BarChart()
            data = Reference(worksheet=sheet,
                             min_row=1,
                             max_row=len(cells)+1,
                             min_col=2,
                             max_col=2)
            chart.add_data(data, titles_from_data=True)
            categories = Reference(worksheet=sheet,
                                   min_row=2,
                                   max_row=len(cells),
                                   min_col=1,
                                   max_col=1)
            chart.set_categories(categories)
            chart.x_axis.title = "Barcode"
            chart.y_axis.title = "Sales Volume"

            # Add the barchart to the sheet, starting on cell E2
            sheet.add_chart(chart, "E2")
            # Save it as transaction_barchart.xlsx
            wb.save("transaction_barchart.xlsx")
        except Exception as e:
            # If an error occurred, display an appropriate message
            print(f'Unable to open table. {e}')
        finally:
            # If it passes or not, the database closes
            db.close()

    def displayExcelReportOfTransactions(self):
        data = self.listAllTransactions()
        cells = list()
        db = sqlite3.connect(self.__databaseName)
        cursor = db.cursor()
        # Add to the list 'cells' the date of transaction, barcode, name, and price of product sold
        for i, j in enumerate(data):
            cursor.execute('''SELECT name FROM products WHERE barcode=?;''', (j.get_barcode(), ))
            name = cursor.fetchone()
            cells.insert(i, [j.get_date(), j.get_barcode(), name[0], j.get_amount()])
        db.close()
        # Add the headings to the top of the list
        cells.insert(0, ["Date", "Barcode", "Name", "Quantity"])
        print(cells)

        # Create the workbook and add each row of data to it
        wb = Workbook()
        sheet = wb.active
        for i in cells:
            sheet.append(i)
        # Save the report
        wb.save("transaction_report.xlsx")

    def addTransactionToDB(self, _transaction=Transaction):
        try:
            db = sqlite3.connect(self.__databaseName)
            cursor = db.cursor()
            # Takes the transaction data and adds it to fields
            transactionDate = _transaction.get_date()
            transactionBarcode = _transaction.get_barcode()
            transactionAmount = _transaction.get_amount()
            # Adds it to the transactions table
            cursor.execute('''INSERT INTO transactions VALUES (?,?,?);''', (transactionDate, transactionBarcode, transactionAmount))
            db.commit()
        except Exception as e:
            # If it fails, it prints an appropriate error message
            print(f'Failed to add product to database. {e}')
        finally:
            # If it passes or not, the database closes
            db.close()

