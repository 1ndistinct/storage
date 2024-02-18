from datetime import datetime
import hashlib
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
            hash_object = hashlib.md5()
            with open(local_dir, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_object.update(chunk)
            if s3_object["ETag"].strip('"') != hash_object.hexdigest():
                return True  # File has changed
    except Exception as exc:
        if not "(404)" in str(exc):
            logging.exception("uploading file will continue...")
        else:
            logging.error("file missing...")
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
        if files_skipped > 0:
            logging.info(f"Skipped {files_skipped}/{len(files)} in {directory_name} since they have not been modified...")

def restore_from_s3(client:"S3Client",settings:Settings):
    logging.info(f"Attempting to download objects from S3 bucket {settings.s3_bucket_name}...")
    if not os.path.exists(settings.volumes_mount_dir):
        logging.info("volumes not mounted, not restoring anything...")
        return
    items = os.listdir(settings.volumes_mount_dir)
    directories = [item for item in items if os.path.isdir(os.path.join(settings.volumes_mount_dir, item))]
    paginator = client.get_paginator('list_objects_v2')
    response_iterator = paginator.paginate(Bucket=settings.s3_bucket_name)
    
    for page in response_iterator:
        for s3_object in page.get('Contents', []):
            s3_key = s3_object['Key']
            volume = s3_key.split("/")[0]
            if volume not in directories:
                logging.warn(f"not downloading file for volume {volume} because it is not mounted...")
                continue
            local_file_path = os.path.join(settings.volumes_mount_dir, s3_key)
            local_directory = os.path.dirname(local_file_path)
            if not os.path.exists(local_directory):
                os.makedirs(local_directory)

            client.download_file(settings.s3_bucket_name, s3_key, local_file_path)
            logging.info(f"Downloaded object {s3_key} to {local_file_path}")
            os.chmod(local_file_path, 0o777)