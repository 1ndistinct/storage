from datetime import datetime
import logging
import os
from typing import TYPE_CHECKING
from .setup import Settings
if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client

def should_update(client:"S3Client",settings:Settings,bucket_dir:str,local_dir:str):
    try:
        s3_object = client.head_object(Bucket=settings.s3_bucket_name, Key=bucket_dir)
        local_file_mod_time = datetime.fromtimestamp(os.path.getmtime(local_dir))
        if s3_object['LastModified'].replace(tzinfo=None) < local_file_mod_time:
            return True  # File has changed
    except Exception:
        logging.exception("uploading file will continue...")
        return True
    return False

def backup_to_s3(client:"S3Client", settings:Settings):
    logging.info(f"attempting to backup volumes mounted at {settings.volumes_mount_dir}...")
    for path, _, files in os.walk(settings.volumes_mount_dir):
        directory_name = path.replace(f"{settings.volumes_mount_dir}/","")
        logging.info(f"backing up files from dir {directory_name}")
        files_skipped = 0
        for file in files:
            bucket_dir = directory_name+'/'+file
            local_dir = os.path.join(path, file)
            if should_update(client,settings,bucket_dir,local_dir):
                client.upload_file(os.path.join(path, file),settings.s3_bucket_name,bucket_dir)
                continue
            files_skipped+=1
        logging.info(f"Skipped {files_skipped}/{len(files)} in {directory_name} since they have not been modified...")

def restore_from_s3(client:"S3Client",settings:Settings):
    ...