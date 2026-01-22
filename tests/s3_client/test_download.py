from core.s3.s3_handler import S3Handler


def test_download(s3_configuration):
    # ARRANGE
    s3, bucket_name = s3_configuration

    file_name = "file.txt"
    file_content = b"Hello, World!"
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

    # ACT
    s3_handler = S3Handler(bucket_name)
    result = s3_handler.download_file(file_name)

    # ASSERT
    assert result == file_content
