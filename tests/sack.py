from unittest import TestCase
from mezages.sack import Sack
from mezages.path import root_path
from mezages.subject import subject_placeholder


class TestUnionMethod(TestCase):
    '''Tests for the union method in the Sack class'''

    def setUp(self):
        self.sack_instance = Sack({
            root_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
        })

    def test_union_with_mount_path(self):
        '''it unifies from store with a mount point'''

        store_to_union = {
            root_path: {f'{subject_placeholder} must contain only 5 characters'},
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': {
                f'{subject_placeholder} must have the gmail domain',
                f'{subject_placeholder} is not a valid email address',
            },
        }

        expected_results = {
            '%root%': ['Must contain only 5 characters'],
            'gender': ['Is not a valid gender string'],
            'user.%root%': ['Must contain only 5 characters'],
            'user.data.email': ['Is not a valid email address',
                                'Must have the gmail domain'],
            'user.gender': ['Is not a valid gender string'],
        }

        # Act
        self.sack_instance.union(store_to_union, mount_path='user')

        # Assert specific elements
        self.assertDictEqual(self.sack_instance.map, expected_results)

    def test_union_without_mount_path(self):
        '''it unifies messages from store without a mount point'''

        store_to_union = {
            root_path: {f'{subject_placeholder} must contain only 5 characters'},
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': {
                f'{subject_placeholder} must have the gmail domain',
                f'{subject_placeholder} is not a valid email address',
            },
        }

        expected_results = {
            '%root%': ['Must contain only 5 characters'],
            'gender': ['Is not a valid gender string'],
            'data.email': ['Is not a valid email address',
                           'Must have the gmail domain']
        }

        # Act
        self.sack_instance.union(store_to_union)

        # Assert specific elements
        self.assertDictEqual(self.sack_instance.map, expected_results)
