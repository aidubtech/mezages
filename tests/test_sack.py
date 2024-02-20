from mezages import Sack
from tests.base_case import BaseCase


class TestInit(BaseCase):
    '''when initializing a sack instance'''

    def test_set_empty_private_store(self):
        '''it assigns an empty dict to a private store property'''

        self.assertEqual(getattr(Sack(), '_Sack__store'), dict())


class TestStore(BaseCase):
    '''when getting the store content of a sack'''

    def test_returns_store_clone(self):
        '''it returns the correct clone of the store'''

        sack = Sack()

        sack.add_messages(['First test message'], 'data')
        sack.add_messages([{'kind': 'failure', 'summary': 'Second test message'}])

        expected_store = getattr(sack, '_Sack__store')

        self.assertDictDeepEqual(sack.store, expected_store)
        self.assertNotEqual(id(sack.store), id(expected_store))


class TestFlat(BaseCase):
    '''when getting messages as a flat list'''

    def test_returns_flat_list_of_messages(self):
        '''it returns a flat list of messages'''

        sack = Sack()

        sack.add_messages(['First test message'], 'data')
        sack.add_messages([{'kind': 'failure', 'summary': 'Second test message'}])

        self.assertCountEqual(
            sack.flat,
            [
                {
                    'ctx': 'data',
                    'kind': 'notice',
                    'summary': 'First test message',
                    'description': None,
                },
                {
                    'ctx': 'global',
                    'kind': 'failure',
                    'summary': 'Second test message',
                    'description': None,
                },
            ],
        )


class TestMount(BaseCase):
    '''when mounting each path in a sack on a mount path'''

    def setUp(self) -> None:
        self.sack = Sack()

        self.sack.add_messages(['First test message'], 'data')

        self.sack.add_messages([{'kind': 'failure', 'summary': 'Second test message'}])

    def test_mount_on_global_path(self):
        '''it returns without updating the store'''

        self.sack.mount('global')

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'global': {
                    'failure': [
                        {
                            'ctx': 'global',
                            'kind': 'failure',
                            'summary': 'Second test message',
                            'description': None,
                        }
                    ]
                },
                'data': {
                    'notice': [
                        {
                            'ctx': 'data',
                            'kind': 'notice',
                            'summary': 'First test message',
                            'description': None,
                        }
                    ]
                },
            },
        )

    def test_mount_on_non_global_path(self):
        '''it replaces the global path and prefixes other paths'''

        self.sack.mount('test.mount')

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'test.mount': {
                    'failure': [
                        {
                            'ctx': 'test.mount',
                            'kind': 'failure',
                            'summary': 'Second test message',
                            'description': None,
                        }
                    ]
                },
                'test.mount.data': {
                    'notice': [
                        {
                            'ctx': 'test.mount.data',
                            'kind': 'notice',
                            'summary': 'First test message',
                            'description': None,
                        }
                    ]
                },
            },
        )


class TestAddMessages(BaseCase):
    '''when adding one or more messages into a context'''

    def setUp(self) -> None:
        self.sack = Sack()

    def test_add_string_message(self) -> None:
        '''it reshapes the string message and correctly add it into the store'''

        self.assertEqual(self.sack.store, dict())

        self.sack.add_messages(['First global message'])

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'global': {
                    'notice': [
                        {
                            'ctx': 'global',
                            'kind': 'notice',
                            'summary': 'First global message',
                            'description': None,
                        }
                    ]
                },
            },
        )

    def test_add_structured_message(self) -> None:
        '''it reshapes the structured message and correctly add it into the store'''

        self.assertEqual(self.sack.store, dict())

        self.sack.add_messages([{'kind': 'failure', 'summary': 'Second global message'}])

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'global': {
                    'failure': [
                        {
                            'ctx': 'global',
                            'kind': 'failure',
                            'summary': 'Second global message',
                            'description': None,
                        }
                    ]
                },
            },
        )

    def test_add_message_for_a_non_existing_context(self) -> None:
        '''it adds the context and adds the message into the right bucket under it'''

        self.assertEqual(self.sack.store, dict())

        self.sack.add_messages(['First global message'], 'some.context')

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'some.context': {
                    'notice': [
                        {
                            'ctx': 'some.context',
                            'kind': 'notice',
                            'summary': 'First global message',
                            'description': None,
                        }
                    ]
                },
            },
        )

    def test_add_message_for_an_existing_context(self) -> None:
        '''it appends the message into the right bucket under it'''

        self.assertEqual(self.sack.store, dict())
        self.sack.add_messages(['Existing context message'], 'some.context')

        self.sack.add_messages(['New context message'], 'some.context')
        self.sack.add_messages(
            [{'kind': 'warning', 'summary': 'Another new message'}], 'some.context'
        )

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'some.context': {
                    'notice': [
                        {
                            'ctx': 'some.context',
                            'kind': 'notice',
                            'summary': 'Existing context message',
                            'description': None,
                        },
                        {
                            'ctx': 'some.context',
                            'kind': 'notice',
                            'summary': 'New context message',
                            'description': None,
                        },
                    ],
                    'warning': [
                        {
                            'ctx': 'some.context',
                            'kind': 'warning',
                            'summary': 'Another new message',
                            'description': None,
                        },
                    ],
                },
            },
        )


class TestMerge(BaseCase):
    '''when merging another sack into the current one'''

    def setUp(self) -> None:
        self.sack = Sack()

    def test_merge_with_global_context(self) -> None:
        '''it merges other Sack into the global context'''

        other_sack = Sack()
        other_sack.add_messages(['First test message'], 'first')
        other_sack.add_messages(
            [{'kind': 'failure', 'summary': 'Second test message'}], 'second'
        )

        self.sack.merge(other_sack)

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'global.first': {
                    'notice': [
                        {
                            'ctx': 'first',
                            'kind': 'notice',
                            'summary': 'First test message',
                            'description': None,
                        }
                    ]
                },
                'global.second': {
                    'failure': [
                        {
                            'ctx': 'second',
                            'kind': 'failure',
                            'summary': 'Second test message',
                            'description': None,
                        }
                    ]
                },
            },
        )

    def test_merge_with_custom_context(self) -> None:
        '''it merges other Sack into a custom context'''

        other_sack = Sack()
        other_sack.add_messages(['First test message'], 'first')
        other_sack.add_messages([{'kind': 'failure', 'summary': 'Second test message'}])

        self.sack.merge(other_sack, mount_context_path='user')

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'user.first': {
                    'notice': [
                        {
                            'ctx': 'first',
                            'kind': 'notice',
                            'summary': 'First test message',
                            'description': None,
                        }
                    ]
                },
                'user.global': {
                    'failure': [
                        {
                            'ctx': 'global',
                            'kind': 'failure',
                            'summary': 'Second test message',
                            'description': None,
                        }
                    ]
                },
            },
        )

    def test_merge_with_existing_context(self) -> None:
        '''it merges other Sack into an existing context'''

        existing_sack = Sack()
        existing_sack.add_messages(['Existing message'], 'existing_context')

        other_sack = Sack()
        other_sack.add_messages(['Other message'], 'existing_context')

        self.sack.merge(existing_sack)
        self.sack.merge(other_sack)

        self.assertDictDeepEqual(
            self.sack.store,
            {
                'global.existing_context': {
                    'notice': [
                        {
                            'ctx': 'existing_context',
                            'kind': 'notice',
                            'summary': 'Existing message',
                            'description': None,
                        },
                        {
                            'ctx': 'existing_context',
                            'kind': 'notice',
                            'summary': 'Other message',
                            'description': None,
                        },
                    ]
                }
            },
        )
