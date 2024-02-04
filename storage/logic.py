import logging
import os
from typing import TYPE_CHECKING
from .setup import Settings
if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


def backup_to_s3(client:"S3Client", settings:Settings):
    logging.info(f"attempting to backup volumes mounted at {settings.volumes_mount_dir}...")
    items = os.listdir(settings.volumes_mount_dir)
    for item in items:
        if os.path.isdir(os.path.join(settings.volumes_mount_dir, item)):
            logging.info(f"backing up {item}...")
            # client.upload_file(f"{root}/{dir}",settings.s3_bucket_name,dir)
    


def restore_from_s3(client:"S3Client",settings:Settings):
    ...