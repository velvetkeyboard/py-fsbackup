import os
import yaml
import boto3

class FsBackup(object):

    def __init__(self, config_path):
        self.config = yaml.safe_load(open('config.yaml', 'r'))
        self.dry_run = False

    def get_s3_client(self):
        session = boto3.Session(profile_name=self.config['aws']['profile'])
        s3 = session.client('s3')
        return s3

    def create_bucket(self):
        s3 = self.get_s3_client()
        s3.create_bucket(
            Bucket=self.config['aws']['bucket'],
            )

    def delete_bucket(self):
        s3 = self.get_s3_client()
        resp = s3.delete_bucket(
            Bucket='string'
        )

    def backup(self, device_name):
        s3 = self.get_s3_client()
        bucket = self.config['aws']['bucket']
        files_for_upload = []
        for entry in self.config['backups'][device_name]:
            entry = os.path.expanduser(entry)
            if os.path.isfile(entry):
                file_path_s3 = device_name + entry
                files_for_upload.append((entry, file_path_s3))
            else:
                for root, dirs, files in os.walk(entry):
                    for file in files:
                        file_path = os.path.expanduser(os.path.join(root, file))
                        file_path_s3 = device_name + file_path
                        files_for_upload.append((file_path, file_path_s3))
        
        for entry in files_for_upload:
            if not self.dry_run:
                print(f"Uploading {entry[0]} to s3://{entry[1]}")
                s3.put_object(
                    Bucket=bucket,
                    Body=open(entry[0], 'rb').read(),
                    Key=entry[1],
                    )


if __name__ == '__main__':
    fsbackup = FsBackup('config.yaml')
    # fsbackup.delete_bucket()
    fsbackup.create_bucket()
    fsbackup.backup('fedora')