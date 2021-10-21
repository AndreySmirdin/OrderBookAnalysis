import numpy as np
import numpy.testing as npt
import unittest
from src.book import calculate_execution_prices


class TestCalculateExecutionPrices(unittest.TestCase):
    mid = 1
    prices = [3, 4, 5]
    amounts = [1, 1, 5]

    def test_execute_first_level_only(self):
        volumes = np.array([2])
        impacts = calculate_execution_prices(self.mid, self.prices, self.amounts, volumes)
        npt.assert_array_almost_equal([3.], impacts)

    def test_execute_last_level(self):
        volumes = np.array([12])
        impacts = calculate_execution_prices(self.mid, self.prices, self.amounts, volumes)
        npt.assert_array_almost_equal([4.], impacts)

    def test_not_enough_orders_in_book(self):
        volumes = np.array([64])
        impacts = calculate_execution_prices(self.mid, self.prices, self.amounts, volumes)
        # Execution price for volume 32 is 32 / 7. Thus, price for volume 64 should be 1 + (32 / 7 - 1) * 2 = 8.14.
        npt.assert_array_almost_equal([8.14], impacts, decimal=2)

    def test_several_volumes(self):
        volumes = np.array([2, 64])
        impacts = calculate_execution_prices(self.mid, self.prices, self.amounts, volumes)
        npt.assert_array_almost_equal([3., 8.14], impacts, decimal=2)
