import unittest
from time import sleep  # Slow down some of these test requests so we don't get limited

from plynk_api import Plynk


class TestPlynk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plynk: Plynk = Plynk(
            username="",
            password="",
            filename="plynk-creds.pkl",
            path="creds",
            proxy_url=None,
            proxy_auth=None
        )
        # Test credentials
        assert cls.plynk.username != "", "Make sure you set your Plynk username inside setUpClass()"
        assert cls.plynk.password != "", "Make sure you set your Plynk password inside setUpClass()"
        # Test login
        try:
            assert cls.plynk.login() is True, "Error during login step"
        except RuntimeError:
            # Force fail if one of our errors is caught
            assert False is True, "Error during login step"
        sleep(5)

    def test_account_number(self):
        self.assertIsInstance(self.plynk.get_account_number(), str, "Error fetching account number")
        sleep(5)

    def test_account_holdings(self):
        self.assertIsInstance(self.plynk.get_account_holdings(self.plynk.get_account_number()), list, "Error fetching account holdings")
        sleep(5)

    def test_account_total(self):
        self.assertIsInstance(self.plynk.get_account_total(self.plynk.get_account_number()), float, "Error fetching account total")
        sleep(5)

    def test_stock_market_open(self):
        self.assertIsInstance(self.plynk.is_stock_market_open(), bool, "Error fetching stock market open")
        sleep(5)

    def test_stock_details(self):
        self.assertIsInstance(self.plynk.get_stock_details("AAPL"), dict, "Error fetching stock details")
        sleep(5)

    def test_stock_search(self):
        self.assertIsInstance(self.plynk.get_stock_search("AAPL"), dict, "Unable to fetch stock search results")
        sleep(5)
        self.assertIsInstance(self.plynk.get_stock_search(query="AAPL", exact=True), dict, "Unable to fetch exact stock search results")
        sleep(5)

    def test_stock_tradable(self):
        self.assertTrue(self.plynk.is_stock_tradable("AAPL"), "Error fetching if AAPL is tradable")  # This should be tradable
        sleep(5)
        self.assertFalse(self.plynk.is_stock_tradable("IWM"), "Error fetching if IWM is tradable")  # This should not be tradable
        sleep(5)

    def test_stock_price(self):
        self.assertIsInstance(self.plynk.get_stock_price("AAPL"), float, "Error fetching stock price")
        sleep(5)

    def test_stock_logo(self):
        self.assertIsInstance(self.plynk.get_stock_logo("AAPL"), str, "Error fetching stock logo")
        sleep(5)

    def test_place_order_price_dry(self):
        try:
            self.assertIsInstance(self.plynk.place_order_price(self.plynk.get_account_number(), "AAPL", 1.0451479, "BUY", "market", True), dict, "Error placing dry price market buy")
        except RuntimeError as e:
            # If the RuntimeError is raised, check if it's about the stock market not being open
            self.assertEqual(str(e), "Stock market is not open")
        sleep(5)
        try:
            self.assertIsInstance(self.plynk.place_order_price(self.plynk.get_account_number(), "AAPL", 12345, "SELL", "market", True), dict, "Error placing dry price market sell")
        except RuntimeError as e:
            # If the RuntimeError is raised, check if it's about the stock market not being open
            self.assertEqual(str(e), "Stock market is not open")
        sleep(5)
        # TODO 10/30/24 Add limit tests once limit functionality is added.

    def test_place_order_quantity_dry(self):
        try:
            self.assertIsInstance(self.plynk.place_order_quantity(self.plynk.get_account_number(), "AAPL", 1.0451479, "BUY", "market", True), dict, "Error placing dry quantity market buy")
        except RuntimeError as e:
            # If the RuntimeError is raised, check if it's about the stock market not being open
            self.assertEqual(str(e), "Stock market is not open")
        sleep(5)
        try:
            self.assertIsInstance(self.plynk.place_order_price(self.plynk.get_account_number(), "AAPL", 112345, "SELL", "market", True), dict, "Error placing dry quantity market sell")
        except RuntimeError as e:
            # If the RuntimeError is raised, check if it's about the stock market not being open
            self.assertEqual(str(e), "Stock market is not open")
        sleep(5)
        # TODO 10/30/24 Add limit tests once limit functionality is added.


if __name__ == '__main__':
    unittest.main()
