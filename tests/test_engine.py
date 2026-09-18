import unittest

from fox.engine import signal_from_prices


class SignalEngineTests(unittest.TestCase):
    def test_warmup(self):
        result = signal_from_prices([1.0] * 19)
        self.assertEqual(result["signal"], "WARMUP")

    def test_buy(self):
        prices = [1.0] * 15 + [1.01] * 5
        self.assertEqual(signal_from_prices(prices)["signal"], "BUY")

    def test_sell(self):
        prices = [1.0] * 15 + [0.99] * 5
        self.assertEqual(signal_from_prices(prices)["signal"], "SELL")

    def test_wait(self):
        self.assertEqual(signal_from_prices([1.0] * 20)["signal"], "WAIT")


if __name__ == "__main__":
    unittest.main()
