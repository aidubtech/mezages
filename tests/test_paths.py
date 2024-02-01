from tests.base_case import BaseCase
from mezages import ROOT_PATH, SUBJECT_PLACEHOLDER

from mezages.paths import (
    is_path,
    PathError,
    ensure_path,
    get_token_type,
    get_subject_type,
    gen_path_children,
    get_path_first_child,
    get_subject_substitute,
    get_subject_parent_type,
)


class TestIsPath(BaseCase):
    '''when checking the validity of paths'''

    def test_with_a_valid_value(self):
        '''it returns true for valid paths'''

        self.assertTrue(is_path(ROOT_PATH))
        self.assertTrue(is_path('0'))
        self.assertTrue(is_path('data'))
        self.assertTrue(is_path('[0]'))
        self.assertTrue(is_path('{4}'))
        self.assertTrue(is_path('{data}'))
        self.assertTrue(is_path('data.[0].{users}.{0}'))

    def test_with_an_invalid_value(self):
        '''it returns false for invalid paths'''

        self.assertFalse(is_path('[user]'))
        self.assertFalse(is_path('%base%'))
        self.assertFalse(is_path('[data].{name}'))
        self.assertFalse(is_path('data.%user%.{name}'))
        self.assertFalse(is_path('data.{user}.roles.[0]'))


class TestEnsurePath(BaseCase):
    '''when ensuring that a value is indeed a path'''

    def test_with_a_valid_value(self):
        '''it returns back the path if it is valid'''

        path = 'data.[0].{users}.[0].{role}'
        self.assertEqual(path, ensure_path(path))

    def test_with_an_invalid_value(self):
        '''it raises an error if path is not valid'''

        path = 'data.[0].[users].{0}.roles.[0]'

        with self.assertRaises(PathError) as error:
            ensure_path(path)

        message = f'{repr(path)} is an invalid path'
        self.assertEqual(str(error.exception), message)


class TestGetTokenType(BaseCase):
    '''when getting the type for a token'''

    def test_key_type_token(self):
        '''it returns `key` for tokens of key type'''

        self.assertEqual(get_token_type('{_}'), 'key')
        self.assertEqual(get_token_type('{10}'), 'key')
        self.assertEqual(get_token_type('{data}'), 'key')

    def test_index_type_token(self):
        '''it returns `index` for tokens of index type'''

        self.assertEqual(get_token_type('[0]'), 'index')
        self.assertEqual(get_token_type('[10]'), 'index')
        self.assertEqual(get_token_type('[550]'), 'index')

    def test_unknown_type_token(self):
        '''it returns `unknown` for tokens of unknown type'''

        self.assertEqual(get_token_type('_'), None)
        self.assertEqual(get_token_type('10'), None)
        self.assertEqual(get_token_type('data'), None)


class TestPathSubjectsFunctions(BaseCase):
    '''when calling path subjects with sack state functions'''

    def setUp(self):
        self.sack_state = {
            ROOT_PATH: {f'{SUBJECT_PLACEHOLDER} must contain only 5 characters'},
            'data': {f'{SUBJECT_PLACEHOLDER} is not a valid record instance'},
            'data.{user}': {f'{SUBJECT_PLACEHOLDER} is not a valid record instance'},
            'data.{user}.{emails}': {'This is not a valid email address array'},
            'data.{user}.{emails}.[0]': {'This must have the gmail domain in its value'},
        }

    def test_gen_path_children(self):
        '''it generate each child path of path in a sack state'''

        self.assertCountEqual(list(gen_path_children(ROOT_PATH, self.sack_state)), [
            'data',
            'data.{user}',
            'data.{user}.{emails}',
            'data.{user}.{emails}.[0]',
        ])

        self.assertCountEqual(list(gen_path_children('data', self.sack_state)), [
            'data.{user}',
            'data.{user}.{emails}',
            'data.{user}.{emails}.[0]',
        ])

        self.assertCountEqual(list(gen_path_children('data.{user}', self.sack_state)), [
            'data.{user}.{emails}',
            'data.{user}.{emails}.[0]',
        ])

        self.assertCountEqual(list(gen_path_children('data.{user}.{emails}', self.sack_state)), [
            'data.{user}.{emails}.[0]',
        ])

        path_children_generator = gen_path_children('data.{user}.{emails}.[0]', self.sack_state)
        self.assertCountEqual(list(path_children_generator), list())

    def test_get_path_first_child(self):
        '''it returns the first child path of path or none if has no children'''

        self.assertEqual(get_path_first_child(ROOT_PATH, self.sack_state), 'data')
        self.assertEqual(get_path_first_child('data', self.sack_state), 'data.{user}')

        path_first_child = get_path_first_child('data.{user}', self.sack_state)
        self.assertEqual(path_first_child, 'data.{user}.{emails}')

        path_first_child = get_path_first_child('data.{user}.{emails}', self.sack_state)
        self.assertEqual(path_first_child, 'data.{user}.{emails}.[0]')

        self.assertEqual(get_path_first_child('data.{user}.{emails}.[0]', self.sack_state), None)

    def test_get_subject_type(self):
        '''it returns the custom type for a path's subject in a sack state'''

        self.assertEqual(get_subject_type(ROOT_PATH, self.sack_state), None)
        self.assertEqual(get_subject_type('data', self.sack_state), 'record')
        self.assertEqual(get_subject_type('data.{user}', self.sack_state), 'record')
        self.assertEqual(get_subject_type('data.{user}.{emails}', self.sack_state), 'array')
        self.assertEqual(get_subject_type('data.{user}.{emails}.[0]', self.sack_state), None)

    def test_get_subject_parent_type(self):
        '''it returns the custom type for a path's parent subject in a sack state'''

        self.assertEqual(get_subject_parent_type(ROOT_PATH, self.sack_state), None)
        self.assertEqual(get_subject_parent_type('data', self.sack_state), None)
        self.assertEqual(get_subject_parent_type('data.{user}', self.sack_state), 'record')
        self.assertEqual(get_subject_parent_type('data.{user}.{emails}', self.sack_state), 'record')

        subject_path = 'data.{user}.{emails}.[0]'
        self.assertEqual(get_subject_parent_type(subject_path, self.sack_state), 'array')

    def test_get_subject_substitute(self):
        '''it returns a string substitute for known type subjects, but returns none for others'''

        self.assertEqual(get_subject_substitute(ROOT_PATH, self.sack_state), None)
        self.assertEqual(get_subject_substitute('data', self.sack_state), 'data')
        self.assertEqual(get_subject_substitute('data.{user}', self.sack_state), 'user in data')

        subject_path = 'data.{user}.{emails}'
        subject_substitute = 'emails in data.{user}'
        self.assertEqual(get_subject_substitute(subject_path, self.sack_state), subject_substitute)

        subject_path = 'data.{user}.{emails}.[0]'
        self.assertEqual(get_subject_substitute(subject_path, self.sack_state), subject_path)
