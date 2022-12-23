from CheckoutRegister import CheckoutRegister


def main():
    cr = CheckoutRegister()

    barcode = input("Please enter the barcode of your item: ")
    try:
        cr.scan_item(barcode)
    except IndexError:
        print("ERROR!! - scanned barcode is incorrect")

    while True:
        cont = input("Would you like to scan another item? (Y/N): ").upper()
        if cont != "Y":
            break
        barcode = input("Please enter the barcode of your item: ")
        try:
            cr.scan_item(barcode)
        except IndexError:
            print("ERROR!! - scanned barcode is incorrect")

    to_pay = input(f'Payment due: ${cr.get_due():3.2f} Please enter an amount to pay: ')
    try:
        if_payed = cr.accept_payment(to_pay)
    except (TypeError, ValueError):
        print("ERROR!! - negative amounts are not accepted")
        if_payed = False

    while not if_payed:
        to_pay = input(f'Payment due: ${cr.get_due():3.2f} Please enter an amount to pay: ')
        try:
            if_payed = cr.accept_payment(to_pay)
        except (TypeError, ValueError):
            print("ERROR!! - negative amounts are not accepted")
            if_payed = False

    cr.print_receipt()


main()
