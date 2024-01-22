import unittest;

from mezages import Mezages

class TestMezagesMerge(unittest.TestCase):
    def setUp(self):
        # Initialize instances for testing
        self.M1 = Mezages({
            'base': ['{entity} must be a string'],
            'data.email': ['{entity} is not a valid email address'],
        })

        self.M2 = Mezages({
            'base': ['{entity} must contain only 5 characters'],
            'gender': ['{entity} is not a valid gender string'],
            'data.email': [
                '{entity} is not a valid email address',
                '{entity} must have the gmail domain',
            ],
        })

    def test_merge_without_mount_point(self):
        # Merge M2 into M1 without a mount point
        self.M1.merge(self.M2, None)

        # Verify the merged result
        expected_result = Mezages({
            'base': [
                '{entity} must be a string',
                '{entity} must contain only 5 characters'
            ],
            'gender': ['{entity} is not a valid gender string'],
            'data.email': [
                '{entity} is not a valid email address',
                '{entity} must have the gmail domain',
            ],
        })

        self.assertEqual(self.M1.map, expected_result.map)

    def test_merge_with_mount_point(self):
        # Merge M2 into M1 with a mount point
        self.M1.merge(self.M2, mount_path='user')

        # Verify the merged result
        expected_result = Mezages({
            'base': ['{entity} must be a string'],
            'data.email': ['{entity} is not a valid email address'],
            'user.base': ['{entity} must contain only 5 characters'],
            'user.gender': ['{entity} is not a valid gender string'],
            'user.data.email': [
                '{entity} is not a valid email address',
                '{entity} must have the gmail domain',
            ],
        })

        self.assertEqual(self.M1.map, expected_result.map)

if __name__ == '__main__':
    unittest.main()
