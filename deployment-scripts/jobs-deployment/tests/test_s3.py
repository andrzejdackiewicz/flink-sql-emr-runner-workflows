import sys
import unittest

import boto3
from moto import mock_s3


sys.path.insert(0, "../")
from .test_s3_utils import put_object
from s3 import get_latest_object


class TestS3(unittest.TestCase):
    @mock_s3
    def test_should_return_latest_object_in_given_location(self):
        # given
        s3 = boto3.resource("s3", region_name="us-east-1")
        bucket = s3.create_bucket(Bucket="mybucket")
        # put the oldest object
        put_object(bucket, key="base/savepoints/sample-query-1/1/savepoint-438ed8-5a70b22243a2/_metadata")
        # put the older object
        put_object(bucket, key="base/savepoints/sample-query-1/1/savepoint-b82705-0242ac120002/_metadata")
        # put an old object
        put_object(bucket, key="base/savepoints/sample-query-1/1/savepoint-38bb51-26fd2296c7a5/_metadata")

        # when
        latest_object = get_latest_object("mybucket", "base/savepoints/sample-query-1/1/")

        # then
        self.assertIsNotNone(latest_object)
        self.assertEqual(latest_object[0], "base/savepoints/sample-query-1/1/savepoint-38bb51-26fd2296c7a5/_metadata")

    @mock_s3
    def test_should_return_latest_object_in_given_location_matching_filtering_predicate(self):
        # given
        s3 = boto3.resource("s3", region_name="us-east-1")
        bucket = s3.create_bucket(Bucket="mybucket")
        put_object(bucket, key="base/chks/q2/1/aa18345e22b4b5c0e49051d1369bd24f/chk-19975_$folder$")
        put_object(bucket, key="base/chks/q2/1/aa18345e22b4b5c0e49051d1369bd24f/chk-19975/_metadata")
        put_object(bucket, key="base/chks/q2/1/aa18345e22b4b5c0e49051d1369bd24f/chk-19976_$folder$")
        put_object(bucket, key="base/chks/q2/1/aa18345e22b4b5c0e49051d1369bd24f/chk-19976/_metadata")
        put_object(bucket, key="base/chks/q2/1/aa18345e22b4b5c0e49051d1369bd24f/shared_$folder$")
        put_object(bucket, key="base/chks/q2/1/aa18345e22b4b5c0e49051d1369bd24f/taskowned_$folder$")

        # when
        latest_object = get_latest_object("mybucket", "base/chks/q2/1/", lambda r: r.endswith("_metadata"))

        # then
        self.assertIsNotNone(latest_object)
        self.assertEqual(latest_object[0], "base/chks/q2/1/aa18345e22b4b5c0e49051d1369bd24f/chk-19976/_metadata")
