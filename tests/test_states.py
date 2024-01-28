from tests.base_case import BaseCase
from mezages import ROOT_PATH, SUBJECT_PLACEHOLDER

from mezages.states import (
    StateError,
    ensure_state,
    validate_state,
    is_valid_state,
)


class TestIsValidState(BaseCase):
    '''when checking the validity of states'''

    def test_with_a_valid_value(self):
        '''it returns true for valid states'''

        self.assertTrue(is_valid_state(
            {
                ROOT_PATH: [
                    'This is seen as a complete message',
                    'This {subject} message is also complete',
                ],
                'gender': (
                    '{subject} message is a partial message',
                    f'{SUBJECT_PLACEHOLDER} makes message partial',
                ),
                'data.{name}': {
                    'This subject placeholder {subject} will be ignored when formatting',
                    f'{SUBJECT_PLACEHOLDER} will not be, but this {{subject}} will be ignored',
                },
            }
        ))

    def test_with_an_invalid_value(self):
        '''it returns false for invalid states'''

        self.assertFalse(is_valid_state(
            {
                ROOT_PATH: [1, 'some message here'],
                'gender': ('first message', ['Another message here']),
                'data.{name}': 'some message outside a collection',
            }
        ))


class TestEnsureState(BaseCase):
    '''when ensuring to make a value into a state'''

    def test_with_a_valid_value(self):
        '''it returns back the bucket as a set if it is valid'''

        state = {
            ROOT_PATH: [
                'This is seen as a complete message',
                'This {subject} message is also complete',
            ],
            'data.{name}': (
                '{subject} message is a partial message',
                f'{SUBJECT_PLACEHOLDER} makes message partial',
            ),
        }

        self.assertDictDeepEqual(ensure_state(state), {
            ROOT_PATH: {
                'This is seen as a complete message',
                'This {subject} message is also complete',
            },
            'data.{name}': {
                '{subject} message is a partial message',
                f'{SUBJECT_PLACEHOLDER} makes message partial',
            },
        })

    def test_with_an_invalid_value(self):
        '''it raises an error if bucket is not valid'''

        state = {
            ROOT_PATH: [1, 'Some complete message here'],
            'data.{name}': 'Some complete message outside array',
            'gender.[name]': ['Some complete message outside collection'],
        }

        with self.assertRaises(StateError) as error:
            ensure_state(state)

        failures = error.exception.data['failures']

        self.assertCountEqual(failures, {
            "'gender.[name]' is an invalid path",
            "'data.{name}' is mapped to an invalid bucket",
            f'{repr(ROOT_PATH)} is mapped to an invalid bucket',
        })


class TestValidateState(BaseCase):
    '''when running state validations on values'''

    def test_with_a_valid_value(self):
        '''it returns an empty set of failure messages'''

        state = {
            ROOT_PATH: [
                'This is seen as a complete message',
                'This {subject} message is also complete',
            ],
            'data.{name}': (
                '{subject} message is a partial message',
                f'{SUBJECT_PLACEHOLDER} makes message partial',
            ),
        }

        self.assertEqual(validate_state(state), set())

    def test_with_an_invalid_value(self):
        '''it returns a set of correct failure messages'''

        state = {
            ROOT_PATH: [1, 'Some complete message here'],
            'data.{name}': 'Some complete message outside array',
            'gender.[name]': ['Some complete message outside collection'],
        }

        self.assertCountEqual(validate_state(state), {
            "'gender.[name]' is an invalid path",
            "'data.{name}' is mapped to an invalid bucket",
            f'{repr(ROOT_PATH)} is mapped to an invalid bucket',
        })
