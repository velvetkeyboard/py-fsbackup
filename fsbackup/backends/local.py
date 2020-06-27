import os
import shutil
from fsbackup.backends.lib import Backend


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
