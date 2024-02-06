from typing import cast
from mezages.paths import PathError
from mezages.subjects import get_subject_substitute
from tests.base_case import BaseCase
from mezages.states import State, StateError
from mezages import Sack, ROOT_PATH, SUBJECT_PLACEHOLDER


class TestInit(BaseCase):
    '''when creating new instances of the sack class'''

    def test_with_no_init_state(self):
        '''it starts with an empty state when no initial state is provided'''

        self.assertEqual(Sack().state, dict())

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
        self.assertMatchState(init_state, sack.state)

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

    def test_the_state_property(self):
        '''it returns a copy of the private state within a sack'''

        copy_state = self.sack.state
        private_state = getattr(self.sack, '_Sack__state')

        self.assertDictDeepEqual(copy_state, private_state)
        self.assertNotEqual(id(copy_state), id(private_state))

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


class TestMerge(BaseCase):
    '''when merging a state with a sack state'''

    def setUp(self):
        self.sack = Sack({
            ROOT_PATH: [f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'],
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': ('This is not a valid email address',)
        })

    def test_with_empty_state(self):
        '''it leaves the sack state unchanged'''

        self.sack.merge(dict())

        self.assertDictDeepEqual(self.sack.state, {
            ROOT_PATH: {f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'},
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': {'This is not a valid email address'},
        })

    def test_with_invalid_state(self):
        '''it raises an error with validation failures'''

        invalid_state = cast(State, {
            ROOT_PATH: 'some invalid message bucket',
            'data.email': (5, 'Must have the gmail domain'),
        })

        with self.assertRaises(StateError) as error:
            self.sack.merge(invalid_state)

        failures = error.exception.data['failures']

        self.assertCountEqual(failures, {
            "'data.email' is mapped to an invalid bucket",
            f'{repr(ROOT_PATH)} is mapped to an invalid bucket',
        })

    def test_with_invalid_mount_path(self):
        '''it raises an error about the invalid mount path'''

        with self.assertRaises(PathError) as error:
            self.sack.merge(dict(), mount_path='users.[i]')

        expected_message = "'users.[i]' is an invalid path"
        self.assertEqual(str(error.exception), expected_message)

    def test_with_no_mount_path(self):
        '''it merges state into sack with child paths unprefixed'''

        new_state = cast(State, {
            ROOT_PATH: ['This is a complete message for root subject'],
            'data.{name}': {f'{SUBJECT_PLACEHOLDER} must be a string value'},
        })

        self.sack.merge(new_state)

        self.assertDictDeepEqual(self.sack.state, {
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

        new_state = cast(State, {
            ROOT_PATH: ['This is a complete message for new data'],
            '{email}': {f'{SUBJECT_PLACEHOLDER} must be registered'},
        })

        self.sack.merge(new_state, 'data')

        self.assertDictDeepEqual(self.sack.state, {
            ROOT_PATH: {f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'},
            'data': {'This is a complete message for new data'},
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': {
                'This is not a valid email address',
                f'{SUBJECT_PLACEHOLDER} must be registered',
            }
        })


class TestMount(BaseCase):
    '''when mounting a path to a sack state'''

    def setUp(self):
        self.sack = Sack({
            ROOT_PATH: [f'{SUBJECT_PLACEHOLDER} must contain only 5 chars'],
            'gender': {f'{SUBJECT_PLACEHOLDER} is not a valid gender'},
            'data.{email}': ('This is not a valid email address',)
        })

    def test_mount_renames_root_path(self):
        '''it renames the root path'''

        self.sack.mount('user')

        self.assertEqual(self.sack.map, {
            'user': ['Must contain only 5 chars'],
            'user.gender': ['Is not a valid gender'],
            'user.data.{email}': ['This is not a valid email address'],
        }
        )

    def test_mount_prefixes_child_path(self):
        '''it prefixes the child path with the root path'''

        self.sack.mount('dataset')

        self.assertEqual(self.sack.map, {
            'dataset': ['Must contain only 5 chars'],
            'dataset.gender': ['Is not a valid gender'],
            'dataset.data.{email}': ['This is not a valid email address']}
        )

    def test_mount_preserves_substitute(self):
        '''it ensures the subject substitute maintain it path linages'''

        self.instance = Sack({
            ROOT_PATH: {f'{SUBJECT_PLACEHOLDER} message'},
            'user.{name}': {'message'},
        })
        self.instance.mount('data')

        self.assertEqual(get_subject_substitute(
            'data.user.{name}', self.instance.state), 'Name in data.user')

    def test_mount_handle_invalid_path(self):
        '''it raises error with validation failure'''

        with self.assertRaises(PathError) as error:
            self.sack.mount('')

        expected_message = "'' is an invalid path"

        self.assertEqual(str(error.exception), expected_message)

    def test_mount_root_path(self):
        '''it mount the root path, when the mount is equal to the ROOT_PATH'''

        self.sack.mount('%root%')

        self.assertEqual(self.sack.map, {
            '%root%': ['Must contain only 5 chars'],
            '%root%.gender': ['Is not a valid gender'],
            '%root%.data.{email}': ['This is not a valid email address']
        })
