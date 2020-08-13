import os


class Backend(object):
    name = None

    def __init__(self, config):
        self.config = config

    def get_name(self):
        return self.name

    def get_config(self):
        if os.path.exists(self.config):
            with open(os.path.expanduser(self.config), 'r') as f:
                _, file_extension = os.path.splitext(self.config)
                if file_extension in ['.yaml', '.yml']:
                    import yaml
                    return yaml.safe_load(f)['backend'][self.get_name()]
                elif file_extension == '.json':
                    import json
                    return json.load(f)['backends'][self.get_name()]

    def upload(self, file_path, name=None):
        raise NotImplementedError

    def download(self, idx):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError
