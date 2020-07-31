import unittest

import operators.mutation as m


class TestMutation(unittest.TestCase):

    def test_random_mutate(self):
        genes = [0, 1, 0.1, 0.9]
        new_genes = m.random_mutate(genes, 1)
        self.assertEqual(len(genes), len(new_genes))
        self.assertGreaterEqual(new_genes, [0, 0, 0, 0])
        self.assertLessEqual(new_genes, [1, 1, 1, 1])
        # print(new_genes)

    def test_partial_abs(self):
        genes = [0, 1, 0.5, 0.25]
        for _i in range(100):
            new_genes = m.partial_abs(genes, 1)
            self.assertEqual(len(genes), len(new_genes))
            self.assertGreaterEqual(new_genes, [-1, 0, -0.5, -0.75])
            self.assertLessEqual(new_genes, [1, 2, 1.5, 1.25])

    def test_partial_relative(self):
        genes = [0, 1, 0.5, 0.25]
        for _i in range(100):
            new_genes = m.partial_relative(genes, 1, 0.02)
            self.assertEqual(len(genes), len(new_genes))
            self.assertGreaterEqual(new_genes, [0.0, 0.8, 0.4, 0.20])
            self.assertLessEqual(new_genes, [0.0, 1.2, 0.6, 0.30])

    def test_vector_abs(self):
        genes = [0, 1, 0.5, 0.25]
        for _i in range(100):
            new_genes = m.vector_abs(genes, 1)
            self.assertEqual(len(genes), len(new_genes))
            self.assertGreaterEqual(new_genes, [-1, 0, -0.5, -0.75])
            self.assertLessEqual(new_genes, [1, 2, 1.5, 1.25])

    def test_vector_relative(self):
        genes = [0, 1, 0.5, 0.25]
        for _i in range(100):
            new_genes = m.vector_relative(genes, 1, 0.02)
            self.assertEqual(len(genes), len(new_genes))
            self.assertGreaterEqual(new_genes, [0.0, 0.8, 0.4, 0.20])
            self.assertLessEqual(new_genes, [0.0, 1.2, 0.6, 0.30])
