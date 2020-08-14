from setuptools import setup, find_packages
from fsbackup import __version__
from fsbackup import __app_name__
from fsbackup import __author__
from fsbackup import __author_email__
from fsbackup import __license__
from fsbackup import __description__


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name=__app_name__,
    version=__version__,
    url='https://gitlab.com/velvetkeyboard/py-fsbackup',
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    description=__description__,
    long_description=long_description,
    install_requires=[
        'PyYAML==5.1.2',
    ],
    extras_require={
        'google_drive': [
            'fsbackup-googledrive-backend',
        ],
        'aws_s3': [
            'fsbackup-aws-backend',
        ],
        'crypto': [
            'python-gnupg==0.4.6',
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "fsbackup=fsbackup.cli:main"
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
