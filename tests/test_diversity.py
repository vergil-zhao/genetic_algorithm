import unittest

from operators.diversity import *


class TestDiversity(unittest.TestCase):

    def setUp(self) -> None:
        self.chromosomes = [
            [0.00, 0.00],
            [0.01, 0.01],
            [0.99, 0.99],
            [0.98, 0.98],
            [0.97, 0.97],
            [0.96, 0.96],
        ]

    def test_divcon_a(self):
        self.assertListEqual(
            divcon_a(self.chromosomes, 0.1, 0.1),
            [0.5, 0.5, 0.25, 0.25, 0.25, 0.25]
        )
