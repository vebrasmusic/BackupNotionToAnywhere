# Backup Notion To Anywhere!
Code for backing up Notion. Runs on a docker container in your VM, 
or you could port it to something like a [Lambda function.](https://aws.amazon.com/lambda/)
## How it works
The internal script gathers all pages in the workspace and exports them as JSON files, with any children pages exported
under folders with the parent's name. This internally runs once a week, exports as a zip file. Need to add
the part that uploads to Synology.

### Credit
The initial code for scraping from Notion was adapted from [here.](https://notionbackups.com/guides/automated-notion-backup-api)

## Future Goals
- Add more storage types (S3, Google Drive, etc.)
- Split out into classes for composition
- download and store files, not just JSON
- build tool for porting JSON > HTML

## Notion setup
1. Go to https://www.notion.so/profile/integrations/
2. Create a new internal integration associated to your workspace
3. Get the internal integration secret, save it somewhere secure
4. Go to Notion, to the top-most page. In page options, go to Connections and select your new integration.
5. This is needed to give the right permissions to the integration.

## Installation
Run the docker build command:
```bash
docker build -t notion-backup .
```

Then, to run you'll need access to the integration's secret key. Run with:
```bash
docker run \
-e INTERNAL_INTEGRATION_SECRET="your_internal_secret" \
-e SERVER_IP_ADDRESS="your_server_ip" \
-e SERVER_PORT="your_server_port" \
-e SERVER_USERNAME="your_username" \
-e SERVER_PASSWORD="your_pw" \
-e DEST_PATH="backup_destination_path" \
-d notion-backup
```

# Caveat
These are Synology DSM specific instructions. I will be building upon this soon
for other backup methods like S3, Google Drive, etc.