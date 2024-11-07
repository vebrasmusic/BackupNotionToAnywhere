import os
import datetime
import time
import shutil
from unittest import case

from dotenv import load_dotenv
from backup.notion import Notion
from storage.s3 import S3
from storage.synology import Synology
import logging
import argparse

logger = logging.getLogger("app_logger")
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
load_dotenv()

# Set up the argument parser
parser = argparse.ArgumentParser(description="BackupNotionToAnywhere")
# parser.add_argument("--arg1", help="First argument", required=True)
parser.add_argument("--storage", help="Which storage repository to upload your backups to", default="s3")

# Parse the arguments
args = parser.parse_args()

while True:
    print(f'Starting backup for {datetime.date.today().isoformat()}.')
    notion = Notion()
    [folder_name, upload_file] = notion.backup()

    if args.storage == "synology":
        storage = Synology()
    elif args.storage == "s3":
        storage = S3()
    storage.upload_backup(upload_file)
    # Optionally, remove the original folder after zipping
    shutil.rmtree(folder_name)
    os.remove(upload_file)
    print(
        f"Backup for {datetime.date.today().isoformat()} completed. Waiting for next scheduled backup."
    )

    # Wait one week (7 days * 24 hours * 60 minutes * 60 seconds)
    time.sleep(1 * 24 * 60 * 60)

