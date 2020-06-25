# FS Backup

cli to help backing up files from your battlestation

## Install

- git

```
git clone https://github.com/velvetkeyboard/py-fsbackup && \
    cd py-fsbackup && \
    pip install --user .
```

## Usage

Using the bellow YAML code as our `~/.fsbackup.yaml`:

```
backends:
  local:
    path: ~/my-backups
schemas:
  my_pc:
    - ~/.bashrc
    - ~/.vimrc
```

- create and upload a backup using default local backend:

`fsbackup upload -s my_pc -b local`

resulting in: `~/my-backups/fsbackup-my_pc-2020-06-24T20:57:57.975172.zip`

- create and upload a backup using default local backend with gpg encryption:

`fsbackup upload -s my_pc -b local -e`

resulting in: `~/my-backups/fsbackup-my_pc-2020-06-24T20:57:57.975172.zip.gpg`


### Backends

- Implemented:
  - local: Local Filesystem

- Not Implemented:
  - aws: AWS S3
  - gdrive: Google Drive

## License

MIT License

Copyright (c) 2020 Ramon Moraes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

