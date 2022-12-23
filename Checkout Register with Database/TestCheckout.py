import unittest
from CheckoutRegister import CheckoutRegister


class TestCheckoutRegister(unittest.TestCase):
    """Tests for Self-Service Checkout Mock-up"""

    def setUp(self):
        self.checkout_register = CheckoutRegister()

    def test_scan_item_error(self):
        """checks if raises an error when given an incorrect barcode"""
        with self.assertRaises(IndexError):
            self.checkout_register.scan_item("999")

    def test_accept_payment_type_error(self):
        """Checks if alphabetical characters raise a TypeError"""
        with self.assertRaises(TypeError):
            self.checkout_register.accept_payment("Alpha")

    def test_accept_payment_value_error(self):
        """Checks if negative number raises a ValueError"""
        with self.assertRaises(ValueError):
            self.checkout_register.accept_payment("-20")

    def test_accept_payment_insufficient_funds(self):
        """Checks if when the amount given is smaller than the total it returns false"""
        self.checkout_register.scan_item("123")
        self.checkout_register.scan_item("123")
        boolean = self.checkout_register.accept_payment("4")
        self.assertFalse(boolean)

    def test_accept_payment(self):
        """Checks if it returns true if amount given is larger than total"""
        self.checkout_register.scan_item("123")
        self.checkout_register.scan_item("123")
        boolean = self.checkout_register.accept_payment("20")
        self.assertTrue(boolean)


if __name__ == "__main__":
    unittest.main()