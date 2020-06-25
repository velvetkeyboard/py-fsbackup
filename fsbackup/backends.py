import os
import shutil
# 3rd Party
import yaml


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
        raise NotImplementedError


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
        ex_path = os.path.expanduser(path)
        for root, dirs, files in os.walk(ex_path):
            for f_path in files:
                ex_f_path = os.path.join(root, f_path)
                yield ex_f_path
