"""
Entrypoint to the application
"""
import argparse
from .setup import setup_logging,get_settings
from .logic import backup_to_s3,restore_from_s3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="entrypoint options.")

    # Add arguments and options to the parser
    parser.add_argument(
        "entrypoint",
        help="which entrypoint to use.",
        choices=["backup","restore"],
    )
    args = parser.parse_args()
    settings = get_settings()
    setup_logging(settings)
    if args.entrypoint == "backup":
        backup_to_s3(settings)
    elif args.entrypoint == "restore":
        restore_from_s3(settings)