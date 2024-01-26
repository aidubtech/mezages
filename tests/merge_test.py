import unittest
from mezages.sack import Sack

class TestSackMerge(unittest.TestCase):
    def test_merge_without_mount_path(self):
        sack1 = Sack({'path1': {'message1', 'message2'}})
        sack2 = Sack({'path2': {'message3'}})
        sack1.merge(sack2, mount_path=None)

        expected_store = {
            'path1': {'message1', 'message2'},
            'path2': {'message3'}
        }
        self.assertEqual(sack1._Sack__store, expected_store)  # type: ignore

    def test_merge_with_mount_path(self):
        sack1 = Sack({'path1': {'message1', 'message2'}})
        sack2 = Sack({'path2': {'message3'}})
        sack1.merge(sack2, mount_path='prefix')

        expected_store = {
            'path1': {'message1', 'message2'},
            'prefix.path2': {'message3'}
        }
       
        self.assertEqual(sack1._Sack__store, expected_store)  # type: ignore

if __name__ == '__main__':
    unittest.main()
