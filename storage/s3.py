import logging
import os

import boto3
from botocore.exceptions import ClientError

from storage.storage import StorageInterface

class S3(StorageInterface):
    def __init__(self):
        self.logger = logging.getLogger("app_logger")

        if (not os.getenv("AWS_ACCESS_KEY_ID")
                or not os.getenv("AWS_SECRET_ACCESS_KEY")):
            raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are not set.")

    def upload_backup(self, file_name):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        bucket = os.getenv("BUCKET_NAME")
        object_name = os.getenv("OBJECT_NAME")
        if not bucket:
            raise ValueError("BUCKET_NAME is not set.")

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client('s3')
        self.logger.info("Beginning S3 upload process.")
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
            self.logger.debug(response)
        except ClientError as e:
            self.logger.error(e)
            return False
        return True