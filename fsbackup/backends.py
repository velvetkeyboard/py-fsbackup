import os
import sys
import datetime
import zipfile
import getpass
import shutil
# 3rd Party
from tqdm import tqdm
import yaml
import boto3
import gnupg


class Backend(object):
   
    name = None

    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.name

    def get_config(self):
        with open(os.path.expanduser(self.config), 'r') as f: 
            return yaml.safe_load(f)['backend'][self.get_name()]

    def upload(self, file_path, name=None):
        raise NotImplemented


class LocalBackend(Backend):

    name = 'local'

    def upload(self, file_path, name=None):
        cfg = self.get_config()
        dest_path = os.path.expanduser(cfg['path'])
        os.makedirs(dest_path, exist_ok=True)
        dest_path += f'/{os.path.basename(file_path)}'
        print(f'Copying {file_path} to {dest_path}')
        shutil.copyfile(file_path, dest_path)

    def list(self):
        cfg = self.get_config()
        dest_path = os.path.expanduser(cfg['path'])
        return self.get_file_paths(dest_path)

    def download(self, idx):
        for i, file_path in enumerate(self.list()):
            if i == idx:
                dest_path = os.path.join(
                        os.getcwd(),
                        os.path.basename(file_path),
                        )
                print(f'Copying {file_path} to {dest_path}')
                shutil.copyfile(file_path, dest_path)
                break

    def get_file_paths(self, path):
        cfg = self.get_config()
        ex_path = os.path.expanduser(path)
        print('ex_path', ex_path)
        for root, dirs, files in os.walk(ex_path):
            for f_path in files:
                ex_f_path = os.path.join(root, f_path)
                yield ex_f_path


class AwsS3Backend(Backend):

    name = 'aws'

    def __init__(self, config_path):
        self.config = yaml.safe_load(open('config.yaml', 'r'))
        self.dry_run = False

    def upload(self, file_path, name=None):
        pass

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
        self.file_uploader(files_for_upload)

    def file_uploader(self, files_for_upload):
        s3 = self.get_s3_client()
        bucket = self.config['aws']['bucket']
        for entry in files_for_upload:
            if not self.dry_run:
                print(f"Uploading {entry[0]} to s3://{entry[1]}")
                s3.put_object(
                    Bucket=bucket,
                    Body=open(entry[0], 'rb').read(),
                    Key=entry[1],
                    )
