from tests.base_case import BaseCase
from mezages.states import StateError
from mezages import Sack, ROOT_PATH, SUBJECT_PLACEHOLDER


class TestInit(BaseCase):
    '''when creating new instances of the sack class'''

    def test_with_no_init_state(self):
        '''it starts with an empty state when no initial state is provided'''

        sack = Sack()
        self.assertEqual(self.get_sack_state(sack), dict())

    def test_with_a_valid_init_state(self):
        '''it starts with a good state when a valid initial state is provided'''

        init_state = {
            ROOT_PATH: [f'{SUBJECT_PLACEHOLDER} must contain only 5 characters'],
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender string'},
            'data.email': (
                f'{SUBJECT_PLACEHOLDER} is not a valid email address',
                f'{SUBJECT_PLACEHOLDER} must have the gmail domain'
            ),
        }

        sack = Sack(init_state)
        expected_state = self.get_sack_state(sack)
        self.assertMatchState(init_state, expected_state)

    def test_with_an_invalid_init_state(self):
        '''it raises a state error when an invalid init state is provided'''

        with self.assertRaises(StateError) as error:
            Sack({
                ROOT_PATH: 'some invalid message bucket',
                'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender string'},
                'data.email': (5, f'{SUBJECT_PLACEHOLDER} must have the gmail domain'),
            })

        failures = error.exception.data['failures']

        self.assertCountEqual(failures, {
            "'data.email' is mapped to an invalid bucket",
            f'{repr(ROOT_PATH)} is mapped to an invalid bucket',
        })


class TestProperties(BaseCase):
    '''when accessing properties on sack instances'''

    def setUp(self):
        self.sack = Sack({
            ROOT_PATH: [f'{SUBJECT_PLACEHOLDER} must contain only 5 characters'],
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender string'},
            'data.{email}': (
                f'{SUBJECT_PLACEHOLDER} must have the gmail domain',
                f'{SUBJECT_PLACEHOLDER} is not a valid email address',
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

        return self.assertDictDeepEqual(self.sack.map, {
            ROOT_PATH: ['Must contain only 5 characters'],
            'gender': ['Is not a valid gender string'],
            'data.{email}': [
                'data.{email} must have the gmail domain',
                'data.{email} is not a valid email address',
            ],
        })
