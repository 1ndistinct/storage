import os
from mypy_boto3_s3 import S3Client
from .setup import Settings


def backup_to_s3(client:S3Client, settings:Settings):
    for root, dirs, _ in os.walk(settings.volumes_mount_dir):
        for dir in dirs:
            client.upload_file(f"{root}/{dir}",settings.s3_bucket_name,dir)
    


def restore_from_s3(client:S3Client,settings:Settings):
    ...