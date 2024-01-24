from mezages.sack import Sack
from mezages.path import root_path
from mezages.store import StoreError
from tests.base_case import BaseCase
from mezages.subject import subject_placeholder


class TestInit(BaseCase):
    '''when creating new instances of the sack class'''

    def test_with_no_input_store(self):
        '''it starts with an empty store when no input store is provided'''

        sack = Sack()
        self.assertEqual(self.get_sack_store(sack), dict())

    def test_with_a_valid_input_store(self):
        '''it starts with a good store when a valid input store is provided'''

        input_store = {
            root_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': (
                f'{subject_placeholder} is not a valid email address',
                f'{subject_placeholder} must have the gmail domain'
            ),
        }

        sack = Sack(input_store)
        expected_store = self.get_sack_store(sack)
        self.assertMatchStore(input_store, expected_store)

    def test_with_an_invalid_input_store(self):
        '''it raises a store error when an invalid input store is provided'''

        with self.assertRaises(StoreError) as error:
            Sack({
                root_path: 'some invalid message bucket',
                'gender': {f'{subject_placeholder} is not a valid gender string'},
                'data.email': (5, f'{subject_placeholder} must have the gmail domain'),
            })

        failures = error.exception.data['failures']

        self.assertCountEqual(failures, {
            "'data.email' is mapped to an invalid bucket",
            f'{repr(root_path)} is mapped to an invalid bucket',
        })


class TestProperties(BaseCase):
    '''when accessing properties on sack instances'''

    def setUp(self):
        self.sack = Sack({
            root_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.{email}': (
                f'{subject_placeholder} must have the gmail domain',
                f'{subject_placeholder} is not a valid email address',
            ),
        })

    def test_the_all_property(self):
        '''it returns a flat list of formatted messages for an entire sack'''

        self.assertCountEqual(self.sack.all, [
            'Must contain only 5 characters',
            'Is not a valid gender string',
            'data.{email} must have the gmail domain',
            'data.{email} is not a valid email address',
        ])

    def test_the_map_property(self):
        '''it returns a dict of paths to lists of formatted messages for an entire sack'''

        result = self.sack.map

        # Extract the below into a custom assert method

        expected_result_keys = [root_path, 'gender', 'data.{email}']
        self.assertCountEqual(list(result.keys()), expected_result_keys)

        for path, messages in result.items():
            if path == root_path:
                self.assertCountEqual(messages, ['Must contain only 5 characters'])

            if path == 'gender':
                self.assertCountEqual(messages, ['Is not a valid gender string'])

            if path == 'data.{email}':
                self.assertCountEqual(messages, [
                    'data.{email} must have the gmail domain',
                    'data.{email} is not a valid email address',
                ])
