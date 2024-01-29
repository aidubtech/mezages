from mezages import ROOT_PATH
from tests.base_case import BaseCase

from mezages.subjects import (
    get_subject_type,
    get_subject_substitute,
    get_subject_parent_type,
    get_subject_first_child_path,
)


class TestSubjects(BaseCase):
    '''when executing functions in the subjects module'''

    def setUp(self):
        self.state = {
            ROOT_PATH: {'some message'},
            'user': {'some message'},
            'user.{name}': {'some message'},
            'user.{roles}': {'some message'},
            'user.{roles}.[0]': {'some message'},
        }

    def test_get_subject_first_child_path(self):
        '''it returns the first child path if any, otherwise returns none'''

        self.assertEqual(get_subject_first_child_path(ROOT_PATH, self.state), 'user')
        self.assertEqual(get_subject_first_child_path('user', self.state), 'user.{name}')
        self.assertEqual(get_subject_first_child_path('user.{name}', self.state), None)

        result = get_subject_first_child_path('user.{roles}', self.state)
        self.assertEqual(result, 'user.{roles}.[0]')

        self.assertEqual(get_subject_first_child_path('user.{roles}.[0]', self.state), None)

    def test_get_subject_type(self):
        '''it returns a type string or none for the subject and ignores invalid child paths'''

        self.assertEqual(get_subject_type(ROOT_PATH, self.state), None)
        self.assertEqual(get_subject_type('user', self.state), 'record')
        self.assertEqual(get_subject_type('user.{name}', self.state), None)
        self.assertEqual(get_subject_type('user.{roles}', self.state), 'array')
        self.assertEqual(get_subject_type('user.{roles}.[0]', self.state), None)

        self.assertEqual(get_subject_type('user.{roles}', self.state, 'user.{roles}.[0]'), 'array')
        self.assertEqual(get_subject_type('user.{roles}', self.state, 'user.{roles}.[10]'), 'array')

    
    def test_get_subject_parent_type(self):
        '''it returns a type string or none for the subject's parent'''

        self.assertEqual(get_subject_parent_type(ROOT_PATH, self.state), None)
        self.assertEqual(get_subject_parent_type('user', self.state), None)
        self.assertEqual(get_subject_parent_type('user.{name}', self.state), 'record')
        self.assertEqual(get_subject_parent_type('user.{roles}', self.state), 'record')
        self.assertEqual(get_subject_parent_type('user.{roles}.[0]', self.state), 'array')

    def test_get_subject_substitute(self):
        '''it returns a string substitute for known type subjects, but returns none for others'''

        self.assertEqual(get_subject_substitute(ROOT_PATH, self.state), None)
        self.assertEqual(get_subject_substitute('user', self.state), 'user')
        self.assertEqual(get_subject_substitute('user.{name}', self.state), 'user.{name}')
        self.assertEqual(get_subject_substitute('user.{roles}', self.state), 'user.{roles}')
        self.assertEqual(get_subject_substitute('user.{roles}.[0]', self.state), 'user.{roles}.[0]')
