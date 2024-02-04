import logging
import os
from typing import TYPE_CHECKING
from .setup import Settings
if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


def backup_to_s3(client:"S3Client", settings:Settings):
    for root, dirs, _ in os.walk(settings.volumes_mount_dir):
        logging.info(f"attempting to backup volumes mounted at {root}... these directories are {dirs}")
        for dir in dirs:
            logging.info(f"backing up {dir} mounted at {root}...")
            # client.upload_file(f"{root}/{dir}",settings.s3_bucket_name,dir)
    


def restore_from_s3(client:"S3Client",settings:Settings):
    ...