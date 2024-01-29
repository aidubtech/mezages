from typing import Any
from unittest import TestCase
from mezages.states import State
from mezages.buckets import is_valid_bucket


class BaseCase(TestCase):
    EQUALITY_ASSERT_MAP: dict[tuple[Any, ...], str] = {
        (dict,): 'assertDictDeepEqual',
        (set, list, tuple): 'assertCountEqual',
    }

    def assertMatchState(self, first: Any, state: State) -> None:
        self.assertIsInstance(first, dict)
        self.assertEqual(len(first), len(state))

        for key, value in first.items():
            self.assertIn(key, state)
            self.assertTrue(is_valid_bucket(value))
            self.assertCountEqual(set(value), state[key])

    def assertDictDeepEqual(self, first: Any, second: Any) -> None:
        self.assertIsInstance(first, dict)
        self.assertIsInstance(second, dict)
        self.assertEqual(len(first), len(second))

        for first_key, first_value in first.items():
            self.assertIn(first_key, second)

            second_value = second[first_key]

            self.assertEqual(type(first_value), type(second_value))

            equality_checker_method: str = 'assertEqual'

            for types, method_name in self.EQUALITY_ASSERT_MAP.items():
                if type(first_value) not in types: continue
                equality_checker_method = method_name

            getattr(self, equality_checker_method)(first_value, second_value)
