import os
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

    def download(self, idx):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError
