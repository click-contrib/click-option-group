# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages


ROOT_DIR = pathlib.Path(__file__).parent


def get_version():
    version = {}
    version_file = ROOT_DIR / 'click_option_group' / '_version.py'
    exec(version_file.read_text(), version)
    return version['__version__']


def get_long_description():
    readme = ROOT_DIR / 'README.md'
    return readme.read_text(encoding='utf-8')


setup(
    name='click-option-group',
    version=get_version(),
    packages=find_packages(exclude='tests'),
    python_requires='>=3.6,<4',
    install_requires=[
        'Click>=7.0',
    ],
    url='https://github.com/espdev/click-option-group',
    license='BSD-3-Clause',
    author='Eugene Prilepin',
    author_email='esp.home@gmail.com',
    description='option groups missing in Click',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
)
