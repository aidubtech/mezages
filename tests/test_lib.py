from tests.base_case import BaseCase
from mezages.lib import build_message, ensure_context_path, ContextError


class TestEnsureContextPath(BaseCase):
    '''when validating an input context path'''

    def test_valid_context_path(self):
        '''it returns back the supplied context path'''

        self.assertEqual(ensure_context_path('data'), 'data')
        self.assertEqual(ensure_context_path('email_address'), 'email_address')
        self.assertEqual(ensure_context_path('data.email_address'), 'data.email_address')

    def test_invalid_context_path(self):
        '''it raises a context error with expected message'''

        with self.assertRaises(ContextError) as error:
            ensure_context_path('some$context')

        self.assertEqual(str(error.exception), "Invalid context path: 'some$context'")

        with self.assertRaises(ContextError) as error:
            ensure_context_path(23)

        self.assertEqual(str(error.exception), "Invalid context path: 23")

        with self.assertRaises(ContextError) as error:
            ensure_context_path([1, 2])

        self.assertEqual(str(error.exception), "Invalid context path: [1, 2]")


class TestBuildMessage(BaseCase):
    '''when creating a message from an input message'''

    def test_with_string_input_message(self):
        '''it returns a dict with the expected entries'''

        message = build_message('some.context', 'This is a summary')

        self.assertEqual(
            message,
            {
                'ctx': 'some.context',
                'kind': 'notice',
                'summary': 'This is a summary',
                'description': None,
            },
        )

    def test_input_message_with_kind(self):
        '''it returns a dict with custom kind and other expected entries'''

        message = build_message(
            'some.context', {'kind': 'failure', 'summary': 'This is a summary'}
        )

        self.assertEqual(
            message,
            {
                'ctx': 'some.context',
                'kind': 'failure',
                'summary': 'This is a summary',
                'description': None,
            },
        )

    def test_input_message_with_description(self):
        '''it returns a dict with description and other expected entries'''

        message = build_message(
            'some.context',
            {
                'kind': 'warning',
                'summary': 'This is a summary',
                'description': 'This is description',
            },
        )

        self.assertEqual(
            message,
            {
                'ctx': 'some.context',
                'kind': 'warning',
                'summary': 'This is a summary',
                'description': 'This is description',
            },
        )
