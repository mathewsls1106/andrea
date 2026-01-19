from moto import mock_aws
import pytest
import boto3


@pytest.fixture
def s3_configuracion():
    with mock_aws():
        nombre_bucket = "bucket-general"
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=nombre_bucket)

        yield s3, nombre_bucket
