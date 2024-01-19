from unittest import TestCase

from mezages import (
    Mezages,
    base_path,
    MezagesStore,
    MezagesError,
    subject_placeholder,
)


class TestInits(TestCase):
    '''when creating new instances of mezages'''

    def setUp(self):
        def get_store(mezages: Mezages) -> MezagesStore:
            # This is tightly coupled to implementation which is not great
            return getattr(mezages, '_Mezages__store')

        self.get_store = get_store

    def test_with_no_input_store(self):
        '''it starts with an empty store when no input store is provided'''

        mezages = Mezages()
        self.assertEqual(self.get_store(mezages), {})

    def test_with_a_valid_input_store(self):
        '''it starts with a parsed store when a valid input store is provided'''

        mezages = Mezages({
            base_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': (
                f'{subject_placeholder} is not a valid email address',
                f'{subject_placeholder} must have the gmail domain'
            ),
        })

        self.assertEqual(self.get_store(mezages), {
            base_path: {f'{subject_placeholder} must contain only 5 characters'},
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': {
                f'{subject_placeholder} is not a valid email address',
                f'{subject_placeholder} must have the gmail domain'
            },
        })

    def test_with_an_invalid_input_store(self):
        '''it raises an exception when a valid input store is provided'''

        with self.assertRaises(MezagesError) as error:
            Mezages({
                base_path: 'some invalid message bucket',
                'gender': {f'{subject_placeholder} is not a valid gender string'},
                'data.email': (5, f'{subject_placeholder} must have the gmail domain'),
            })

        exception_message = str(error.exception)
        # Was not able to assert properly due to loss of store order, so these are not good assertions
        # For example, incompletely defined error messages provided here wil still make the assertions pass
        self.assertTrue("[!] '{base}' is not mapped to a valid bucket of messages" in exception_message)
        self.assertTrue("[!] 'data.email' has one or more invalid messages in its bucket" in exception_message)


class TestPropertiesAndMethods(TestCase):
    '''when calling public methods on instances of mezages'''

    def setUp(self):
        self.mezages = Mezages({
            base_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': (
                f'{subject_placeholder} must have the gmail domain',
                f'{subject_placeholder} is not a valid email address',
            ),
        })

    def test_the_all_property(self):
        '''it returns a flat list of formatted messages from all paths'''

        self.assertCountEqual(self.mezages.all, [
            'Must contain only 5 characters',
            'gender is not a valid gender string',
            'data.email must have the gmail domain',
            'data.email is not a valid email address',
        ])

    def test___get_entity_substitute_method(self):
        '''it returns a substitute for the placeholder expected to be user friendly'''

        get_subject_substitute = getattr(self.mezages, '_Mezages__get_subject_substitute')

        self.assertEqual(get_subject_substitute('data.user.email'), 'data.user.email')

    def test___format_messages(self):
        '''it returns a set of messages with the subject placeholders replaced'''

        format_messages = getattr(self.mezages, '_Mezages__format_messages')

        messages = {
            f'{subject_placeholder} must be a valid email address',
            'This is a generic message which must have belonged to base'
        }

        self.assertCountEqual(format_messages('data.email', messages), {
            'data.email must be a valid email address',
            'This is a generic message which must have belonged to base',
        })

    def test___ensure_store_with_a_valid_input_store(self):
        '''it returns a parsed version of the input store provided'''

        ensure_store = getattr(self.mezages, '_Mezages__ensure_store')

        store = {
            base_path: {f'{subject_placeholder} must contain only 5 characters'},
            'gender': [f'{subject_placeholder} is not a valid gender string'],
            'data.email': (
                f'{subject_placeholder} must have the gmail domain',
                f'{subject_placeholder} is not a valid email address',
            ),
        }

        self.assertEqual(ensure_store(store), {
            base_path: {f'{subject_placeholder} must contain only 5 characters'},
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': {
                f'{subject_placeholder} must have the gmail domain',
                f'{subject_placeholder} is not a valid email address',
            },
        })

    def test_with_an_invalid_input_store(self):
        '''it raises an exception for the invalid input store provided'''

        ensure_store = getattr(self.mezages, '_Mezages__ensure_store')

        with self.assertRaises(MezagesError) as error:
            ensure_store({
                base_path: 'some invalid message bucket',
                'gender': {f'{subject_placeholder} is not a valid gender string'},
                'data.email': (5, f'{subject_placeholder} must have the gmail domain'),
            })

        exception_message = str(error.exception)
        # Was not able to assert properly due to loss of store order, so these are not good assertions
        # For example, incompletely defined error messages provided here wil still make the assertions pass
        self.assertTrue("[!] '{base}' is not mapped to a valid bucket of messages" in exception_message)
        self.assertTrue("[!] 'data.email' has one or more invalid messages in its bucket" in exception_message)

    def test_union_without_mount_point(self):
        '''it unifies messages from the store without a mount point'''

        self.mezages.union({
            base_path: [f'{subject_placeholder} must contain only 5 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': (
                f'{subject_placeholder} is not a valid email address',
                f'{subject_placeholder} must have the Gmail domain'
            ),
        })

        self.assertEqual(self.mezages.map, {
            base_path: [
                f'{subject_placeholder} must be a string',
                f'{subject_placeholder} must contain only 5 characters'
            ],
            'gender': [f'{subject_placeholder} is not a valid gender string'],
            'data.email': [
                f'{subject_placeholder} is not a valid email address',  # Duplicates of this message were removed
                f'{subject_placeholder} must have the Gmail domain'
            ],
        })

    def test_union_with_mount_point(self):
        '''it unifies the messages from store with mount point'''

        self.mezages.union({
            base_path: [f'{subject_placeholder} must contain only 3 characters'],
            'gender': {f'{subject_placeholder} is not a valid gender string'},
            'data.email': (
                f'{subject_placeholder} is not a valid email address',
                f'{subject_placeholder} must have the Yahoo domain',
            ),
        }, mount_path='user')

        self.assertEqual(self.mezages.map, {
            'base': [f'{subject_placeholder} must be a string'],
            'data.email': [f'{subject_placeholder} is not a valid email address'],
            'user': [f'{subject_placeholder} must contain only 5 characters'],
            'user.gender': [f'{subject_placeholder} is not a valid gender string'],
            'user.data.email': [
                f'{subject_placeholder} is not a valid email address',
                f'{subject_placeholder} must have the Gmail domain'
            ],
        })
