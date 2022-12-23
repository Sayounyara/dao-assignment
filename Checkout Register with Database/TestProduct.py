import unittest
from Product import Product


class TestProduct(unittest.TestCase):
    """Tests for Product.py"""

    def setUp(self):
        self.product = Product("Test", "12 Kilobytes", 0.23, 101)

    def test_get_name(self):
        """passing"""
        name = self.product.get_name()
        self.assertEqual(name, "Test")

    def test_get_measurements(self):
        """passing"""
        name = self.product.get_measurements()
        self.assertEqual(name, "12 Kilobytes")

    def test_get_price(self):
        """passing"""
        name = self.product.get_price()
        self.assertEqual(name, 0.23)

    def test_get_barcode(self):
        """passing"""
        name = self.product.get_barcode()
        self.assertEqual(name, 101)


if __name__ == "__main__":
    unittest.main()