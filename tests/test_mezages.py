from unittest import TestCase


class TestDummy(TestCase):
    '''when checking out integration between pytest and unittest'''

    def test_it_should_add_the_two_numbers(self):
        self.assertEqual(1 + 1, 2)

    def test_difference_between_integers(self):
        '''it should find the difference between two integers'''
        self.assertEqual(4 - 2, 2)
