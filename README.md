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

# Storage Types
## S3 
For S3, you will run with the following args:
```bash
docker run -d --name notion-backup notion-backup --storage s3
```

### Setup
1. Create a new bucket in the [AWS Console]('https://aws.amazon.com/s3/')
2. Click on the new bucket and click "Permissions"
3. Navigate to "Bucket policy" and click Edit
4. Paste in the following to the policy, changing out with your info:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::account-id:user/username"
                ]
            },
            "Action": ["s3:PutObject", "s3:GetObject"],
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
    ]
} 
```
#### IAM User
If you have never delved into making S3 work and all, it can be a pain. For programmatic access
to S3 you'll need to have created an IAM user with permissions to access the bucket. This can be done
by:
1. Navigating to the IAM page in the AWS console
2. Clicking "Users"
3. Create a new user
4. In "Set Permissions", choose the "Attach policies directly" tab and search for `AmazonS3FullAccess`
5. Create the user!
6. You can now copy / paste the ARN for the previous step.
#### IAM Security Credentials
To get the security credentials for this IAM user, you can:
1. Click the previously created IAM user
2. Select "Security Credentials"
3. Select "Create Access Key"
4. Click "Third Party Service" and click "next"
5. Copy the access key and the secret

### Environment variables
The application will expect `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `BUCKET_NAME`
to be defined in a .env file. 
1. `cd` into the cloned repo.
```bash
cd BackupNotionToAnywhere 
```
2. Create and edit the .env
```bash 
sudo nano .env
```
3. Enter the following:
```bash
AWS_ACCESS_KEY_ID={youraccesskey}
AWS_SECRET_ACCESS_KEY={yoursecretkey}
BUCKET_NAME={yourbucketnnname}
```
4. save and close