from core.s3.s3_handler import S3Handler


def test_delete_file(s3_configuration):
    s3, bucket_name = s3_configuration

    file_name = "file.txt"
    file_content = b"Hello, World!"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
    s3_handler = S3Handler(bucket_name)

    s3_handler.delete_file(file_name)
    sut = s3.list_objects_v2(Bucket=bucket_name)["KeyCount"]
    assert sut == 0
