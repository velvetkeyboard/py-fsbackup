import os
import argparse
import getpass
from fsbackup.lib import FsBackup
from fsbackup.backends import LocalBackend


class BaseAction(argparse.Action):

    def __init__(self, **kwargs):
        super(BaseAction, self).__init__(**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        self.cmd(namespace)

    def cmd(self, namespace):
        raise NotImplementedError(_('.cmd() not defined'))


class Upload(BaseAction):
    def cmd(self, namespace):
        cfg = namespace.config or 'fsbackup.yaml'
        backend = {
            'local': LocalBackend(cfg)
            }[namespace.backend]
        password = None
        if namespace.encryption:
            password = getpass.getpass()
        FsBackup(cfg).backup(
            namespace.schema,
            backend,
            password=password,
            encryption_engine=namespace.encryption,
            )


class Listing(BaseAction):
    def cmd(self, namespace):
        cfg = namespace.config or 'fsbackup.yaml'
        backend = {
            'local': LocalBackend(cfg)
            }[namespace.backend]
        for i, path in enumerate(backend.list()):
            print(f'[{i}] {path}')


class Download(BaseAction):
    def cmd(self, namespace):
        cfg = namespace.config or 'fsbackup.yaml'
        backend = {
            'local': LocalBackend(cfg)
            }[namespace.backend]

        if not namespace.number:
            for i, path in enumerate(backend.list()):
                print(f'[{i}] {path}')
            idx = int(input('Number: '))
        else:
            idx = int(namespace.number)
        backend.download(idx)


def main():
    # -------------------------------------------------------------------[Args]
    parser = argparse.ArgumentParser(
            prog='fsbackup',
            description='backup your files'
            )
    sparser = parser.add_subparsers(help='actions help')
    # -----------------------------------------------------------------[upload]
    upload = sparser.add_parser('upload', help='upload files to a backend')
    upload.add_argument('-c', '--config', type=str, help='config.yml file path')
    upload.add_argument('-s', '--schema', type=str, help="config file's schema to use")
    upload.add_argument('-b', '--backend', type=str, help='service you want to use to upload')
    upload.add_argument('-e', '--encryption', action='store_true', help='encryption engine')
    upload.add_argument('run', nargs=0, action=Upload, help=argparse.SUPPRESS)
    # ---------------------------------------------------------------[Download]
    listing = sparser.add_parser('list', help='download backup files from a backend')
    listing.add_argument('-c', '--config', type=str, help='config.yml file path')
    listing.add_argument('-b', '--backend', type=str, help='service you want to use to upload')
    listing.add_argument('run', nargs=0, action=Listing, help=argparse.SUPPRESS)
    download = sparser.add_parser('download', help='download backup files from a backend')
    download.add_argument('-c', '--config', type=str, help='config.yml file path')
    download.add_argument('-b', '--backend', type=str, help='service you want to use to upload')
    download.add_argument('-n', '--number', type=str, help='number index')
    download.add_argument('run', nargs=0, action=Download, help=argparse.SUPPRESS)
    args = parser.parse_args()


if __name__ == '__main__':
    main()

