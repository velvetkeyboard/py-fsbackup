import os
import sys
import argparse
import datetime
import zipfile
import logging
import getpass
import shutil
# 3rd Party
from tqdm import tqdm
import yaml
import boto3
import gnupg


LOGLEVEL = os.environ.get("FSBACKUP_LOGLEVEL", "INFO")
logger = logging.getLogger('fsbackup')
logger.setLevel(LOGLEVEL)


class FsBackup(object):
    def __init__(self, config):
        self.config = config

    def get_config(self):
        with open(os.path.expanduser(self.config), 'r') as f: 
            return yaml.safe_load(f)

    def get_curr_date(self):
        return datetime.datetime.now().isoformat()

    def backup(self, schema, backend, password=None, encryption_engine=None):
        zfile, zfile_path = self.create_compression_file(schema)
        file_paths = self.get_file_paths(schema)
        for file_path in tqdm(file_paths, ascii=True, desc='Zipping'):
            zfile.write(file_path)
        zfile.close()

        if password and encryption_engine:
            upload_file_path = self.encrypt_archive(
                    zfile_path,
                    password,
                    encryption_engine,
                    )
        else:
            upload_file_path = zfile_path

        backend.upload(upload_file_path)

    def encrypt_archive(self, file_path, passphrase, encryption_engine):
        gpg = gnupg.GPG()
        with open(file_path, 'rb') as f:
            output_file_path = f'{file_path}.gpg'
            status = gpg.encrypt_file(
                f,
                symmetric=True,
                passphrase=passphrase,
                recipients=[],
                output=output_file_path,
                )
            if not status.ok:
                print(f'GPG Ok: {status.ok}')
                print(f'GPG Status: {status.status}')
                print(f'GPG Err: {status.stderr}')
                raise Excpetion(status.stderr)
            return output_file_path

    def create_compression_file(self, schema_name, path=None):
        path = path or '.'
        zfile_name = f'fsbackup-{schema_name}-{self.get_curr_date()}.zip'
        zfile_path = os.path.join(path, zfile_name)
        return zipfile.ZipFile(zfile_path, 'w'), zfile_path


    def get_file_paths(self, schema):
        cfg = self.get_config()
        for path in cfg['schemes'][schema]:
            ex_path = os.path.expanduser(path)
            if os.path.isfile(ex_path):
                yield ex_path
            else:
                for root, dirs, files in os.walk(ex_path):
                    for f_path in files:
                        ex_f_path = os.path.join(root, f_path)
                        yield ex_f_path

