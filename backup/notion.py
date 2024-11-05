import datetime
import json
import os
import shutil
import requests
from tqdm import tqdm


class Notion:
    def __init__(self):
        secret_token = os.getenv("INTERNAL_INTEGRATION_SECRET")
        if not secret_token:
            raise ValueError("INTERNAL_INTEGRATION_SECRET is not set.")
        self.secret_token = secret_token

    def backup(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        folder = 'notion-backup-' + timestamp
        os.mkdir(folder)

        headers = {
            'Authorization': f'Bearer {self.secret_token}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
        }

        response = requests.post('https://api.notion.com/v1/search', headers=headers)

        for block in tqdm(response.json()['results']):
            with open(f'{folder}/{block["id"]}.json', 'w') as file:
                file.write(json.dumps(block))

            child_blocks = requests.get(
                f'https://api.notion.com/v1/blocks/{block["id"]}/children',
                headers=headers,
            )
            if child_blocks.json()['results']:
                os.mkdir(folder + f'/{block["id"]}')

                for child in child_blocks.json()['results']:
                    with open(f'{folder}/{block["id"]}/{child["id"]}.json', 'w') as file:
                        file.write(json.dumps(child))

        # Zip the folder
        shutil.make_archive(folder, 'zip', folder)
        print(f"Backup folder '{folder}' zipped as '{folder}.zip'.")

        return [folder, f"{folder}.zip"]
