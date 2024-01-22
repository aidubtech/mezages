from mezages.path import root_path
from tests.base_case import BaseCase
from mezages.sack import Sack, SackError
from mezages.bucket import subject_placeholder


class TestInit(BaseCase):
    '''when creating new instances of the sack class'''

    def test_with_no_input_store(self):
        '''it starts with an empty store when no input store is provided'''

        self.assertEqual(Sack().store, dict())

    def test_with_a_valid_input_store(self):
        '''it starts with a good store when a valid input store is provided'''

        sack = Sack({
            root_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': (
                f'{subject_placeholder} is not a valid email address',
                f'{subject_placeholder} must have the gmail domain'
            ),
        })

        sack_path_values = list(path.value for path in sack.store.keys())

        self.assertCountEqual(sack_path_values, [root_path, 'gender', 'data.email'])

        for path, bucket in sack.store.items():
            if path.is_root:
                self.assertCountEqual(bucket.value, {f'{subject_placeholder} must contain only 5 characters'})

            if path.value == 'gender':
                self.assertCountEqual(bucket.value, {f'{subject_placeholder} is not a valid gender string'})

            if path.value == 'data.email':
                self.assertCountEqual(bucket.value, {
                    f'{subject_placeholder} is not a valid email address',
                    f'{subject_placeholder} must have the gmail domain'
                })

    def test_with_an_invalid_input_store(self):
        '''it raises an exception when an invalid input store is provided'''

        with self.assertRaises(SackError) as error:
            Sack({
                root_path: 'some invalid message bucket',
                'gender': {f'{subject_placeholder} is not a valid gender string'},
                'data.email': (5, f'{subject_placeholder} must have the gmail domain'),
            })

        self.assertCountEqual(error.exception.data['failures'], {
            f'{repr(root_path)} is not mapped to a valid bucket',
            "'data.email' has one or more invalid messages in its bucket",
        })


class TestBehaviours(BaseCase):
    '''when calling public properties and methods on sack objects'''

    def setUp(self):
        self.sack = Sack({
            root_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': (
                f'{subject_placeholder} must have the gmail domain',
                f'{subject_placeholder} is not a valid email address',
            ),
        })

    def test_the_all_property(self):
        '''it returns a flat list of formatted messages from the entire sack'''

        self.assertCountEqual(self.sack.all, [
            'Must contain only 5 characters',
            'gender is not a valid gender string',
            'data.email must have the gmail domain',
            'data.email is not a valid email address',
        ])

    def test_the_map_property(self):
        '''it returns a dict of path values to lists of formatted messages from the entire sack'''

        result = self.sack.map
        expected_path_values = [root_path, 'gender', 'data.email']

        self.assertCountEqual(list(result.keys()), expected_path_values)

        for path_value, messages in result.items():
            if path_value == root_path:
                self.assertCountEqual(messages, ['Must contain only 5 characters'])

            if path_value == 'gender':
                self.assertCountEqual(messages, ['gender is not a valid gender string'])

            if path_value == 'data.email':
                self.assertCountEqual(messages, [
                    'data.email must have the gmail domain',
                    'data.email is not a valid email address',
                ])
