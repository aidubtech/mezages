from mezages import ROOT_PATH
from tests.base_case import BaseCase

from mezages.subjects import (
    get_subject_substitute,
    get_subject_lineage_types,
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

    def test_get_subject_any_child_path(self):
        '''it returns the first child's path if any, otherwise returns none'''

        self.assertEqual(get_subject_first_child_path(ROOT_PATH, self.state), 'user')
        self.assertEqual(get_subject_first_child_path('user', self.state), 'user.{name}')
        self.assertEqual(get_subject_first_child_path('user.{name}', self.state), None)

        result = get_subject_first_child_path('user.{roles}', self.state)
        self.assertEqual(result, 'user.{roles}.[0]')

        self.assertEqual(get_subject_first_child_path('user.{roles}.[0]', self.state), None)

    def test_get_subject_lineage_types(self):
        '''it returns a tuple for types for each subject in a path, where type can be none'''

        result = get_subject_lineage_types(ROOT_PATH, self.state)
        self.assertCountEqual(result, (None,))

        result = get_subject_lineage_types('user', self.state)
        self.assertCountEqual(result, ('record',))

        result = get_subject_lineage_types('user.{name}', self.state)
        self.assertCountEqual(result, ('record', 'scion'))

        result = get_subject_lineage_types('user.{roles}', self.state)
        self.assertCountEqual(result, ('record', 'array'))

        result = get_subject_lineage_types('user.{roles}.[0]', self.state)
        self.assertCountEqual(result, ('record', 'array', 'scion'))

    def test_get_subject_substitute(self):
        '''it returns a string substitute for known type subjects, but returns none for others'''

        self.assertEqual(get_subject_substitute(ROOT_PATH, self.state), None)
        self.assertEqual(get_subject_substitute('user', self.state), 'user')
        self.assertEqual(get_subject_substitute('user.{name}', self.state), 'user.{name}')
        self.assertEqual(get_subject_substitute('user.{roles}', self.state), 'user.{roles}')
        self.assertEqual(get_subject_substitute('user.{roles}.[0]', self.state), 'user.{roles}.[0]')
