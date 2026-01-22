from core.s3.s3_handler import S3Handler


def test_upload_file(s3_configuration):
    # ARRANGE
    s3, bucket_name = s3_configuration
    file_name = "document.txt"
    content = "hi senior"

    s3.create_bucket(Bucket=bucket_name)
    s3_handler = S3Handler(bucket=bucket_name)

    # ACT
    result = s3_handler.upload_file(name=file_name, content=content)

    # verifica que se haya subido el archivo correctamente
    objects = s3.list_objects_v2(Bucket=bucket_name)
    keys = [obj["Key"] for obj in objects.get("Contents", [])]

    assert result is True
    assert file_name in keys


def test_upload_file_by_path(s3_configuration, tmp_path):
    # ARRANGE
    s3, bucket_name = s3_configuration

    local_file = tmp_path / "my_report.txt"
    local_file.write_text("file content")

    s3_handler = S3Handler(bucket=bucket_name)

    result = s3_handler.upload_file_from_path(file_path=local_file)

    # ASSERT
    objects = s3.list_objects_v2(Bucket=bucket_name)
    keys = [obj["Key"] for obj in objects.get("Contents", [])]
    assert len(keys) == 1
    assert result is True


def test_upload_folder(s3_configuration, tmp_path):
    s3, bucket_name = s3_configuration
    s3_handler = S3Handler(bucket=bucket_name)

    # creamos path temporal
    temp_path = tmp_path / "mi proyecto"

    temp_path.mkdir()
    (temp_path / "file1.txt").write_text("content 1")
    (temp_path / "file2.txt").write_text("content 2")
    # subimos carpeta
    s3_handler.upload_folder(local_path=temp_path)

    # ASSERT
    objects = s3.list_objects_v2(Bucket=bucket_name)
    keys = [obj["Key"] for obj in objects.get("Contents", [])]
    assert "file1.txt" in keys
    assert "file2.txt" in keys
    assert len(keys) == 2
