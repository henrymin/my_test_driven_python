import unittest
from datetime import datetime

from ..stock import Stock


class StockTest(unittest.TestCase):
    def test_price_of_a_new_stock_class_should_be_None(self):
        stock = Stock("GOOG")
        self.assertIsNone(stock.price)

    def test_stock_update(self):
        """An update should set the price on the stock object
        we will be using the 'datetime' module for the timestamp
        """
        goog = Stock("GOOG")
        goog.update(datetime(2018, 5, 10), price=10)
        self.assertEqual(10, goog.price)

    def test_negative_price_should_throw_ValueError(self):
        goog = Stock("GOOG")
        self.assertRaises(ValueError, goog.update, datetime(2018, 5, 10), -1)

    def test_stock_price_should_give_the_latest_price(self):
        goog = Stock("GOOG")
        goog.update(datetime(2018, 5, 12), price=10)
        goog.update(datetime(2018, 5, 11), price=8.4)
        self.assertAlmostEqual(10, goog.price, delta=0.0001)