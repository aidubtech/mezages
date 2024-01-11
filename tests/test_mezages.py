from mezages import Mezages
from tests.test_case import TestCase


class TestMezages(TestCase):
    '''when checking out integration between pytest and unittest'''

    def test_it_should_add_the_two_numbers(self):
        self.assertEqual(Mezages().export(), {})

    def test_find_difference_between_integers(self):
        '''it should find the difference between two integers'''
        self.assertEqual(4 - 2, 2)
