from core.s3.s3_handler import S3Handler


def test_list_objects(s3_configuration):
    """
    return a list of files
    """
    # ARRANGE
    s3, bucket_name = s3_configuration

    s3.put_object(Bucket=bucket_name, Key="file.txt")
    s3.put_object(Bucket=bucket_name, Key="file2.txt")

    # ACT
    s3_handler = S3Handler(bucket=bucket_name)
    result = s3_handler.list_files()

    # ASSERT
    assert isinstance(result, list)
    assert len(result) == 2

    assert "file.txt" in result
    assert "file2.txt" in result
