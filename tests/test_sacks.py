from mezages.paths import PathError
from mezages.sacks import SackError, ensure_sack_state, validate_sack_state
from tests.base_case import BaseCase
from mezages import Sack, ROOT_PATH, SUBJECT_PLACEHOLDER


class TestEnsureState(BaseCase):
    '''when ensuring that a value is indeed a sack state'''

    def test_with_a_valid_value(self):
        '''it returns back the bucket as a set if it is valid'''

        input_sack_state = {
            ROOT_PATH: [
                'This is seen as a complete message',
                'This {subject} message is also complete',
            ],
            'data.{name}': (
                '{subject} message is a partial message',
                f'{SUBJECT_PLACEHOLDER} makes message partial',
            ),
        }

        expected_sack_state = {
            ROOT_PATH: {
                'This is seen as a complete message',
                'This {subject} message is also complete',
            },
            'data.{name}': {
                '{subject} message is a partial message',
                f'{SUBJECT_PLACEHOLDER} makes message partial',
            },
        }

        self.assertDictDeepEqual(ensure_sack_state(input_sack_state), expected_sack_state)

    def test_with_an_invalid_value(self):
        '''it raises an error if bucket is not valid'''

        with self.assertRaises(SackError) as error:
            ensure_sack_state({
                ROOT_PATH: [1, 'Some complete message here'],
                'data.{name}': 'Some complete message outside array',
                'gender.[name]': ['Some complete message outside collection'],
            })

        failures = error.exception.data['failures']

        self.assertCountEqual(failures, {
            "'gender.[name]' is an invalid path",
            "'data.{name}' is mapped to an invalid bucket",
            f'{repr(ROOT_PATH)} is mapped to an invalid bucket',
        })


class TestValidateState(BaseCase):
    '''when running sack state validations on an argument'''

    def test_with_a_valid_value(self):
        '''it returns an empty set of failure messages'''

        input_sack_state = {
            ROOT_PATH: [
                'This is seen as a complete message',
                'This {subject} message is also complete',
            ],
            'data.{name}': (
                '{subject} message is a partial message',
                f'{SUBJECT_PLACEHOLDER} makes message partial',
            ),
        }

        self.assertEqual(validate_sack_state(input_sack_state), set())

    def test_with_an_invalid_value(self):
        '''it returns a set of correct failure messages'''

        invalid_sack_state = {
            ROOT_PATH: [1, 'Some complete message here'],
            'data.{name}': 'Some complete message outside array',
            'gender.[name]': ['Some complete message outside collection'],
        }

        self.assertCountEqual(validate_sack_state(invalid_sack_state), {
            "'gender.[name]' is an invalid path",
            "'data.{name}' is mapped to an invalid bucket",
            f'{repr(ROOT_PATH)} is mapped to an invalid bucket',
        })


class TestInit(BaseCase):
    '''when creating new instances of the sack class'''

    def test_with_no_init_state(self):
        '''it starts with an empty state when no initial state is provided'''

        sack = Sack()
        sack_state = getattr(sack, '_Sack__state')
        self.assertEqual(sack_state, dict())

    def test_with_a_valid_init_state(self):
        '''it starts with a good state when a valid initial state is provided'''

        init_state = {
            ROOT_PATH: [f'{SUBJECT_PLACEHOLDER} must contain only 5 characters'],
            'data': {f'{SUBJECT_PLACEHOLDER} is not a valid record instance'},
        }

        sack = Sack(init_state)
        sack_state = getattr(sack, '_Sack__state')
        self.assertMatchSackState(init_state, sack_state)

    def test_with_an_invalid_init_state(self):
        '''it raises a state error when an invalid init state is provided'''

        with self.assertRaises(SackError) as error:
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
            'data': {f'{SUBJECT_PLACEHOLDER} is not a valid record instance'},
            'data.{email}': (
                f'{SUBJECT_PLACEHOLDER} must have the gmail domain',
                f'{SUBJECT_PLACEHOLDER} is not a valid email address',
            ),
        })

    def test_the_all_property(self):
        '''it returns a flat list of formatted messages for an entire sack'''

        self.assertCountEqual(self.sack.all, [
            'Must contain only 5 characters',
            'data is not a valid record instance',
            'email in data must have the gmail domain',
            'email in data is not a valid email address',
        ])

    def test_the_map_property(self):
        '''it returns a dict of paths to lists of formatted messages for an entire sack'''

        return self.assertDictDeepEqual(self.sack.map, {
            ROOT_PATH: ['Must contain only 5 characters'],
            'data': ['data is not a valid record instance'],
            'data.{email}': [
                'email in data must have the gmail domain',
                'email in data is not a valid email address',
            ],
        })


class TestMerge(BaseCase):
    '''when merging some other sack into a current sack'''

    def setUp(self):
        self.sack = Sack({
            ROOT_PATH: [f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'],
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': ('This is not a valid email address',)
        })

    def test_with_empty_sack(self):
        '''it leaves the sack state unchanged'''

        self.sack.merge(Sack())

        sack_state = getattr(self.sack, '_Sack__state')

        self.assertDictDeepEqual(sack_state, {
            ROOT_PATH: {f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'},
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': {'This is not a valid email address'},
        })

    def test_with_an_invalid_mount_path(self):
        '''it raises an exception for the an invalid mount path'''

        with self.assertRaises(PathError) as error:
            self.sack.merge(Sack(), mount_path='users.[i]')

        expected_message = "'users.[i]' is an invalid path"
        self.assertEqual(str(error.exception), expected_message)

    def test_with_no_mount_path(self):
        '''it merges sack state into the current sack state with child paths unprefixed'''

        other_sack = Sack({
            ROOT_PATH: ['This is a complete message for root subject'],
            'data.{name}': {f'{SUBJECT_PLACEHOLDER} must be a string value'},
        })

        self.sack.merge(other_sack)

        sack_state = getattr(self.sack, '_Sack__state')

        self.assertDictDeepEqual(sack_state, {
            ROOT_PATH: {
                'This is a complete message for root subject',
                f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'
            },
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': {'This is not a valid email address'},
            'data.{name}': {f'{SUBJECT_PLACEHOLDER} must be a string value'},
        })

    def test_with_mount_path(self):
        '''it merges state into sack with child paths prefixed'''

        other_sack = Sack({
            ROOT_PATH: ['This is a complete message for new data'],
            '{email}': {f'{SUBJECT_PLACEHOLDER} must be registered'},
        })

        self.sack.merge(other_sack, 'data')

        sack_state = getattr(self.sack, '_Sack__state')

        self.assertDictDeepEqual(sack_state, {
            ROOT_PATH: {f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'},
            'data': {'This is a complete message for new data'},
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': {
                'This is not a valid email address',
                f'{SUBJECT_PLACEHOLDER} must be registered',
            }
        })
