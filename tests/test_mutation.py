import unittest

import operators.mutation as m


class TestMutation(unittest.TestCase):

    def test_random_mutate(self):
        genes = [0, 1, 0.1, 0.9]
        new_genes = m.random_mutate(genes, 1)
        self.assertEqual(len(genes), len(new_genes))
        self.assertGreaterEqual(new_genes, [0, 0, 0, 0])
        self.assertLessEqual(new_genes, [1, 1, 1, 1])
        print(new_genes)

    def test_norm_dist(self):
        genes = [0, 1, 0.5, 0.25]
        for _i in range(100):
            new_genes = m.norm_dist(genes, 1)
            self.assertEqual(len(genes), len(new_genes))
            self.assertGreaterEqual(new_genes, [-1, 0, -0.5, -0.75])
            self.assertLessEqual(new_genes, [1, 2, 1.5, 1.25])
            print(new_genes)
