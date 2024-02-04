from functools import lru_cache
import logging
import sys
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    s3_bucket_name = ""
    volumes_mount_dir = ""
    log_level:str = "INFO"


@lru_cache
def get_settings():
    return Settings()

def setup_logging(settings:Settings):
    """
    Setup a stream handler to stdout and a file handler
    to write to ./logs/logfile.log from the root logger for convenience
    """
    logger = logging.getLogger()
    logger.setLevel(settings.log_level.upper())
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(processName)-10s | %(levelname)-8s | %(funcName)s | %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger