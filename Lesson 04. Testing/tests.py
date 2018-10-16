import unittest
from gcd import gcd

__version__ = '0.1'


class TestGCD(unittest.TestCase):
    def test_zeros(self):
        self.assertRaises(ValueError, gcd, 0, 0)

    def test_fractional(self):
        self.assertRaises(ValueError, gcd, 2.5, 1)

    def test_coprime_numbers(self):
        cases = {
            (5, 8): 1,
            (16, 27): 1,
            (11, 34): 1
        }
        for params, result in cases.items():
            with self.subTest(case=params):
                self.assertEqual(gcd(*params), result)

    def test_negative(self):
        cases = {
            (1, -1): 1,
            (-32, 0): 32,
            (-64, -64): 64,
            (6, -15): 3
        }
        for params, result in cases.items():
            with self.subTest(case=params):
                self.assertEqual(gcd(*params), result)
