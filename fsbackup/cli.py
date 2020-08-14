import os
import argparse
import getpass
from fsbackup.lib import FsBackup


FSBACKUP_YAML = '~/.fsbackup.yaml'
FSBACKUP_JSON = '~/.fsbackup.json'


def get_backend_by_name(name):
    if name == 'google_drive':
        from fsbackup_googledrive.backends import GoogleDriveBackend
        ret = GoogleDriveBackend
    elif name == 'local':
        from fsbackup.backends import LocalBackend
        ret = LocalBackend
    else:
        from fsbackup.backends import LocalBackend
        ret = LocalBackend
    return ret


def get_cfg_path(config):
    return os.path.expanduser(
            config or FSBACKUP_YAML)


def upload(args):
    cfg = get_cfg_path(args.config)
    backend = get_backend_by_name(args.backend)(cfg)
    password = None
    if args.encryption:
        password = getpass.getpass()
    FsBackup(cfg).backup(
        args.schema,
        backend,
        password=password,
        encryption_engine=args.encryption,
        )


def listing(args):
    cfg = get_cfg_path(args.config)
    backend = get_backend_by_name(args.backend)(cfg)
    for i, path in enumerate(backend.list()):
        print(f'[{i}] {path}')


def download(args):
    cfg = get_cfg_path(args.config)
    backend = get_backend_by_name(args.backend)(cfg)
    if not args.number:
        for i, path in enumerate(backend.list()):
            print(f'[{i}] {path}')
        idx = int(input('Number: '))
    else:
        idx = int(args.number)
    backend.download(idx)


def main():
    # --------------------------------------------------------------------[Args]
    parser = argparse.ArgumentParser(
            prog='fsbackup',
            description='backup your files'
            )
    sparser = parser.add_subparsers(help='actions help')

    # ------------------------------------------------------------------[upload]
    upload_parser = sparser.add_parser(
            'upload', help='upload_parser files to a backend')
    upload_parser.add_argument(
        '-c', '--config', type=str, default=FSBACKUP_YAML, help='config.yml file path')
    upload_parser.add_argument(
        '-s', '--schema', type=str, help="config file's schema to use")
    upload_parser.add_argument(
        '-b', '--backend', type=str, help='service you want to use to upload_parser')
    upload_parser.add_argument(
        '-e', '--encryption', action='store_true', help='encryption engine')
    upload_parser.set_defaults(func=upload)

    # -----------------------------------------------------------------[listing]
    list_parser = sparser.add_parser(
        'list', help='download backup files from a backend')
    list_parser.add_argument(
        '-c', '--config', type=str, default=FSBACKUP_YAML, help='config.yml file path')
    list_parser.add_argument(
        '-b', '--backend', type=str, help='service you want to use to upload')
    list_parser.set_defaults(func=listing)

    # ----------------------------------------------------------------[Download]
    download_parser = sparser.add_parser(
        'download', help='download_parser backup files from a backend')
    download_parser.add_argument(
        '-c', '--config', type=str, default=FSBACKUP_YAML, help='config.yml file path')
    download_parser.add_argument(
        '-b', '--backend', type=str, help='service you want to use to upload')
    download_parser.add_argument(
        '-n', '--number', type=str, help='number index')
    download_parser.set_defaults(func=download)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
