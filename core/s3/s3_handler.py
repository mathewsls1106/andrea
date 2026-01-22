import os
from pathlib import Path
from typing import Any, List, Optional

import boto3


class S3Handler:
    def __init__(self, bucket: str):
        self.bucket_name = bucket
        self.s3 = boto3.client("s3")

    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """
        lists all objects in the bucket
        """
        params = {"Bucket": self.bucket_name}

        if prefix:
            params["Prefix"] = prefix

        response = self.s3.list_objects_v2(**params)

        # returns only the keys of the files
        return [obj["Key"] for obj in response.get("Contents", [])]

    def upload_file(self, name: str, content: Any) -> bool:
        """
        uploads a file to the bucket
        """
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=name, Body=content)
            print("uploaded successfully")
            return True
        except Exception as e:
            print(f"error uploading file: {e}")
            return False

    def upload_file_from_path(self, file_path: Path) -> bool:
        """
        uploads a file to the bucket from a local path
        """
        try:
            self.s3.upload_file(str(file_path), self.bucket_name, file_path.name)
            print("uploaded successfully")
            return True
        except Exception as e:
            print(f"error uploading file: {e}")
            return False

    def download_file(self, file_name: str) -> Optional[bytes]:
        """
        downloads a file from the bucket
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=file_name)
            content = response["Body"].read()
            print("download successful")
            return content
        except Exception as e:
            print(f"error downloading file: {e}")
            return None

    def delete_file(self, file_name: str) -> bool:
        """
        deletes a file from the bucket
        """
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
            print("deletion successful")
            return True
        except Exception as e:
            print(f"error deleting file: {e}")
            return False

    def upload_folder(self, local_path: str) -> bool:
        """
        uploads a folder to the bucket
        """
        base_path = Path(local_path)
        try:
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    full_path = Path(root) / file
                    s3_key = str(full_path.relative_to(base_path))
                    self.s3.upload_file(
                        Filename=str(full_path), Bucket=self.bucket_name, Key=s3_key
                    )
            print("upload successful")
            return True
        except Exception as e:
            print(f"error uploading folder: {e}")
            return False
