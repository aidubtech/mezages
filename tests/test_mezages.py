import unittest


class TestSample(unittest.TestCase):
    'when checking out integration between pytest and unittest'

    def test_it_should_add_the_two_numbers(self):
        self.assertEqual(2 + 2, 4)

    def test_find_difference_between_integers(self):
        'it should find the difference between two integers'
        self.assertEqual(4 - 2, 2)
