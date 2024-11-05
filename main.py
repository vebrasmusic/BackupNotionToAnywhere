import os
import datetime
import time
import shutil
from dotenv import load_dotenv

from backup.notion import Notion
from storage.synology import Synology

load_dotenv()
# for local dev, then we can pass a .env file
# into the root without building in docker

while True:
    print(f'Starting backup for {datetime.date.today().isoformat()}.')
    notion = Notion()
    synology = Synology()
    [folder_name, upload_file] = notion.backup()
    synology.save_to_server(upload_file)
    # Optionally, remove the original folder after zipping
    shutil.rmtree(folder_name)
    os.remove(upload_file)
    print(
        f"Backup for {datetime.date.today().isoformat()} completed. Waiting for next scheduled backup."
    )

    # Wait one week (7 days * 24 hours * 60 minutes * 60 seconds)
    time.sleep(1 * 24 * 60 * 60)

