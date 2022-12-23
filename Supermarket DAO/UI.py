from SupermarketDAO import SupermarketDAO
from Product import Product


def start():
    print('Starting Administrative System.')
    user = __authenticateUser()
    while type(user) == bool:
        user = __authenticateUser()
    print(f'\nWelcome {user}!')
    print('Creating SupermarketDAO...')
    dao = SupermarketDAO('checkout.db')
    print('Done!')

    switch = {
        'a' : __addProductToDB,
        'b' : __listAllProducts,
        'c' : __findProduct,
        'd' : __listAllTransactions,
        'e' : __displayBarchartOfProductsSold,
        'f' : __displayExcelReportOfTransactions
    }
    while True:
        __printCommands()
        command = input('> ')
        if command == 'g':
            break
        if command not in switch.keys():
            print('Unknown command.')
        else:
            switch.get(command)(dao)
    __exit(user)


def __authenticateUser():
    users = __getUsers()
    # Ask for the username
    userName = input('Enter username. > ')
    while userName not in users.keys():
        # While the username doesn't match any key, it continues to ask for a username
        print('User name not found.')
        userName = input('Enter username. > ')
    # Once a correct username has been inputted it then asks for password,
    # or a special command '-back' to go back to inputting usernames
    print("Type '-back' to go back to username.")
    password = input('Enter password. > ')
    while password != users[userName]:
        # If the password was the command '-back', then return False and the start() function
        # will invoke _authenticateUser() again, effectively 'returning' to inputting the
        # username
        if password == '-back':
            return False
        # Or, if the password was incorrect, it will continue to ask for a password
        print('Password not found.')
        password = input('Enter password. > ')
    # Finally, it returns the username field to the start() function
    return userName


def __getUsers():
    users = dict()
    # Opens the users.bin file and adds the users to a dictionary
    with open('users.bin', mode='rb') as file:
        username = None
        isUsername = True
        for line in file:
            data = line.decode()
            data = data[:-1]
            # If the currently selected data is the username, add it to the userName variable and switch to password
            if isUsername:
                userName = data
                isUsername = False
            else:
                # Add the username as a key and the password as the value
                users[userName] = data
                isUsername = True
    # Return the dictionary of users
    return users


def __printCommands():
    # Prints all available commands
    print('\na > Add products to database')
    print('b > List all products in database (ascending order of product barcode')
    print('c > Find a product in the database, based on product barcode')
    print('d > List all transactions (ascending order of date of transaction)')
    print('e > Display a bar chart of products sold by quantity')
    print('f > Display an Excel report of all transactions')
    print('g > Exit')


def __addProductToDB(dao=SupermarketDAO):
    successful = False
    # Allows this to continue until adding a product was successful
    while not successful:
        # Allows the user to enter product information
        productBarcode = input('Enter product barcode > ')
        # Error catching
        if len(productBarcode) > 10:
            print('Barcode must be no greater than 10 characters')
            continue
        productName = input('Enter product name > ')
        # Error catching
        if len(productName) > 10:
            print('Name must be no greater than 10 characters')
            continue
        productDesc = input('Enter product description > ')
        # Error catching
        if len(productDesc) > 255:
            print('Description must be no greater than 255 characters')
            continue
        # Error catching try block to see if product price is valid
        try:
            productPrice = float(input('Enter product price > $'))
        except Exception as e:
            print(f'Invalid price.')
            continue
        finally:
            product = Product(productBarcode, productName, productDesc, productPrice)
        if dao.addProductToDB(product):
            print('Product added successfully.')
            successful = True
        else:
            print('Product was unable to be added to database.')


def __listAllProducts(dao=SupermarketDAO):
    # Invoke the SupermarketDAO version of the function
    products = dao.listAllProducts()
    for i in products:
        print(i)


def __findProduct(dao=SupermarketDAO):
    # Ask the user for a barcode, then see if a product has the inputted barcode
    successful = False
    while not successful:
        barcode = input('Enter barcode > ')
        # Error catching
        if len(barcode) > 10:
            print('Barcode must be no greater than 10 characters')
            continue
        product = dao.findProduct(barcode)
        print(product) if type(product) == Product else print(f'No product with barcode {barcode} found.')


def __listAllTransactions(dao=SupermarketDAO):
    # Invoke the SupermarketDAO version of the function
    transactions = dao.listAllTransactions()
    for i in transactions:
        print(i)


def __displayBarchartOfProductsSold(dao=SupermarketDAO):
    # Invoke the SupermarketDAO version of the function
    dao.displayBarchartOfProductsSold()


def __displayExcelReportOfTransactions(dao=SupermarketDAO):
    # Invoke the SupermarketDAO version of the function
    dao.displayExcelReportOfTransactions()


def __exit(user):
    # Says goodbye to the user and exits the program
    print(f'Goodbye {user}!')
    exit(0)