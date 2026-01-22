from moto import mock_aws
import pytest
import boto3


@pytest.fixture
def s3_configuration():
    with mock_aws():
        bucket_name = "general-bucket"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=bucket_name)

        yield s3, bucket_name