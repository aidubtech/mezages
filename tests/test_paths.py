from tests.base_case import BaseCase
from mezages.paths import is_valid_path, ensure_path, get_token_type, ROOT_PATH, PathError


class TestIsValidPath(BaseCase):
    '''when checking the validity of paths'''

    def test_with_a_valid_value(self):
        '''it returns true for valid paths'''

        self.assertTrue(is_valid_path(ROOT_PATH))
        self.assertTrue(is_valid_path('0'))
        self.assertTrue(is_valid_path('data'))
        self.assertTrue(is_valid_path('[0]'))
        self.assertTrue(is_valid_path('{4}'))
        self.assertTrue(is_valid_path('{data}'))
        self.assertTrue(is_valid_path('data.[0].{users}.{0}'))

    def test_with_an_invalid_value(self):
        '''it returns false for invalid paths'''

        self.assertFalse(is_valid_path('[user]'))
        self.assertFalse(is_valid_path('%base%'))
        self.assertFalse(is_valid_path('[data].{name}'))
        self.assertFalse(is_valid_path('data.%user%.{name}'))


class TestEnsurePath(BaseCase):
    '''when ensuring that a value is indeed a path'''

    def test_with_a_valid_value(self):
        '''it returns back the path if it is valid'''

        path = 'data.[0].{users}.{0}.roles.[0]'
        self.assertEqual(path, ensure_path(path))

    def test_with_an_invalid_value(self):
        '''it raises an error if path is not valid'''

        path = 'data.[0].[users].{0}.roles.[0]'

        with self.assertRaises(PathError) as error:
            ensure_path(path)

        message = f'{repr(path)} is an invalid path'
        self.assertEqual(str(error.exception), message)


class TestGetTokenType(BaseCase):
    '''when getting the type for tokens'''

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
