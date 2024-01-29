from tests.base_case import BaseCase

from mezages.buckets import (
    BucketError,
    ensure_bucket,
    format_bucket,
    is_valid_bucket,
    SUBJECT_PLACEHOLDER,
)


class TestIsValidBucket(BaseCase):
    '''when checking the validity of buckets'''

    def test_with_a_valid_value(self):
        '''it returns true for valid buckets'''

        self.assertTrue(is_valid_bucket([
            'This is seen as a complete message',
            'This {subject} message is also complete',
        ]))

        self.assertTrue(is_valid_bucket((
            '{subject} message is a partial message',
            f'{SUBJECT_PLACEHOLDER} makes message partial',
        )))

        self.assertTrue(is_valid_bucket({
            'This subject placeholder {subject} will be ignored when formatting',
            f'{SUBJECT_PLACEHOLDER} will not be, but this {{subject}} will be ignored',
        }))

    def test_with_an_invalid_value(self):
        '''it returns false for invalid buckets'''

        self.assertFalse(is_valid_bucket(1))
        self.assertFalse(is_valid_bucket([1, 'some message here']))
        self.assertFalse(is_valid_bucket('some message outside a collection'))
        self.assertFalse(is_valid_bucket(('first message', ['Another message here'])))


class TestEnsureBucket(BaseCase):
    '''when ensuring to make a value into a bucket'''

    def test_with_a_valid_value(self):
        '''it returns back the bucket as a set if it is valid'''

        bucket = [
            'This is seen as a complete message',
            'This {subject} message is also complete',
        ]
        self.assertCountEqual(set(bucket), ensure_bucket(bucket))

    def test_with_an_invalid_value(self):
        '''it raises an error if bucket is not valid'''

        bucket = [1, 'some message here']

        with self.assertRaises(BucketError) as error:
            ensure_bucket(bucket)

        message = f'{repr(bucket)} is an invalid bucket'
        self.assertEqual(str(error.exception), message)


class TestFormatBucket(BaseCase):
    '''when formatting buckets with different subject substitutes'''

    def setUp(self):
        self.bucket = {
            '{subject} message is a partial message',
            f'{SUBJECT_PLACEHOLDER} makes message partial',
            'This is some complete message that will not be touched',
        }

    def test_with_no_subject_substitute(self):
        '''it removes the placeholder and uppercase the first character'''

        self.assertCountEqual(format_bucket(self.bucket, None), [
            'Makes message partial',
            'Message is a partial message',
            'This is some complete message that will not be touched',
        ])

    def test_with_subject_substitute(self):
        '''it replaces the subject placeholders with the subject_substitute'''

        self.assertCountEqual(format_bucket(self.bucket, 'data.{users}'), [
            'data.{users} makes message partial',
            'data.{users} message is a partial message',
            'This is some complete message that will not be touched',
        ])
