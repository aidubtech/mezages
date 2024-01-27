from typing import Any
from unittest import TestCase
from mezages.sack import Sack
from mezages.store import Store
from mezages.bucket import Bucket


class BaseCase(TestCase):
    EQUALITY_ASSERT_MAP: dict[tuple[Any, ...], str] = {
        (dict,): 'assertDictDeepEqual',
        (set, list, tuple): 'assertCountEqual',
    }

    def get_sack_store(self, sack: Sack):
        return getattr(sack, '_Sack__store')

    def assertMatchStore(self, first: Any, store: Store):
        self.assertIsInstance(first, dict)
        self.assertEqual(len(first), len(store))

        for key, value in first.items():
            self.assertIn(key, store)
            self.assertTrue(Bucket.is_valid(value))
            self.assertCountEqual(set(value), store[key])

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
