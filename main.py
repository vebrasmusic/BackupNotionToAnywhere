import requests
import os
import datetime
import json
import time
import shutil
from synology_api import filestation, downloadstation
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
# for local dev, then we can pass a .env file
# into the root without building in docker

def backup_notion():
    # Helper function to download files
    def download_file(file_url, download_path):
        file_response = requests.get(file_url, stream=True)
        with open(download_path, 'wb') as file:
            for chunk in file_response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    folder = 'notion-backup-' + timestamp
    os.mkdir(folder)

    secret_token = os.getenv("INTERNAL_INTEGRATION_SECRET")
    if not secret_token:
        raise ValueError("INTERNAL_INTEGRATION_SECRET is not set.")

    headers = {
        'Authorization': f'Bearer {secret_token}',
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
    }

    response = requests.post('https://api.notion.com/v1/search', headers=headers)

    for block in tqdm(response.json()['results']):
        with open(f'{folder}/{block["id"]}.json', 'w') as file:
            file.write(json.dumps(block))

        # # Check if the block contains a file
        # if 'type' in block:
        #     print(block['type'])
        #     if block['type'] == 'file':
        #         file_url = block['file']['file']['url']
        #         file_name = block['file']['file']['url'].split("/")[-1].split("?")[0]  # Extract file name from URL
        #         download_file(file_url, f'{folder}/{file_name}')

        child_blocks = requests.get(
            f'https://api.notion.com/v1/blocks/{block["id"]}/children',
            headers=headers,
        )
        if child_blocks.json()['results']:
            os.mkdir(folder + f'/{block["id"]}')

            for child in child_blocks.json()['results']:
                with open(f'{folder}/{block["id"]}/{child["id"]}.json', 'w') as file:
                    file.write(json.dumps(child))

                # # Check if the child block contains a file
                # if 'type' in child:
                #     print(child['type'])
                #     if child['type'] == 'paragraph':
                #
                #     #
                #     # if child['type'] == 'file':
                #     #     # Extract the file URL and name
                #     #     print("a file! finally")
                #     #     file_url = child['file']['file']['url']
                #     #     file_name = child['file']['file']['url'].split("/")[-1].split("?")[0]  # Extract file name from URL
                #     #     download_file(file_url, f'{folder}/{block["id"]}/{file_name}')

    # Zip the folder
    shutil.make_archive(folder, 'zip', folder)
    print(f"Backup folder '{folder}' zipped as '{folder}.zip'.")

    return [folder, f"{folder}.zip"]

def save_to_server(zip_name):
    ip_address = os.getenv("SERVER_IP_ADDRESS")
    port = os.getenv("SERVER_PORT")
    username = os.getenv("SERVER_USERNAME")
    password = os.getenv("SERVER_PASSWORD")
    dest_path = os.getenv("DEST_PATH")

    fl = filestation.FileStation(ip_address, port,username, password,
                                 secure=False, cert_verify=False,dsm_version=6, debug=True, otp_code=None)

    fl.upload_file(dest_path, zip_name)

while True:
    print(f'Starting backup for {datetime.date.today().isoformat()}.')
    [folder_name, zip_name] = backup_notion()
    save_to_server(zip_name)
    # Optionally, remove the original folder after zipping
    shutil.rmtree(folder_name)
    os.remove(zip_name)
    print("Backup completed. Waiting for next scheduled backup.")

    # Wait one week (7 days * 24 hours * 60 minutes * 60 seconds)
    time.sleep(1 * 24 * 60 * 60)

