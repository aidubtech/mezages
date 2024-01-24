from typing import Any
from unittest import TestCase
from mezages.sack import Sack
from mezages.store import Store
from mezages.bucket import Bucket


class BaseCase(TestCase):
    def get_sack_store(self, sack: Sack):
        return getattr(sack, '_Sack__store')

    def assertMatchStore(self, test_value: Any, expected_value: Store):
        self.assertIsInstance(test_value, dict)
        self.assertCountEqual(list(test_value.keys()), list(expected_value.keys()))

        for path, bucket in test_value.items():
            self.assertTrue(Bucket.is_valid(bucket))
            self.assertCountEqual(set(bucket), expected_value[path])
