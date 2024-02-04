import logging
import os
from typing import TYPE_CHECKING
from .setup import Settings
if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


def backup_to_s3(client:"S3Client", settings:Settings):
    logging.info(f"attempting to backup volumes mounted at {settings.volumes_mount_dir}...")
    for path, _, files in os.walk(settings.volumes_mount_dir):
        directory_name = path.replace(f"{settings.volumes_mount_dir}/","")
        logging.info(f"backing up files from dir {directory_name}")
        for file in files:
            client.upload_file(os.path.join(path, file),settings.s3_bucket_name,directory_name+'/'+file)

def restore_from_s3(client:"S3Client",settings:Settings):
    ...