# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup


PACKAGE_NAME = 'click_option_group'
ROOT_DIR = pathlib.Path(__file__).parent


def get_version():
    version = {}
    version_file = ROOT_DIR / PACKAGE_NAME / '_version.py'
    exec(version_file.read_text(), version)
    return version['__version__']


def get_long_description():
    readme = ROOT_DIR / 'README.md'
    changelog = ROOT_DIR / 'CHANGELOG.md'
    return '{}\n{}'.format(
        readme.read_text(encoding='utf-8'),
        changelog.read_text(encoding='utf-8')
    )


setup(
    name='click-option-group',
    version=get_version(),
    packages=[PACKAGE_NAME],
    python_requires='>=3.6,<4',
    install_requires=[
        'Click>=7.0,<8',
    ],
    extras_require={
        'docs': [
            'sphinx>=2.3',
            'Pallets-Sphinx-Themes',
            'm2r @ git+https://github.com/crossnox/m2r@dev#egg=m2r',
        ],
        'tests': ['pytest'],
    },
    url='https://github.com/click-contrib/click-option-group',
    project_urls={
        "Code": 'https://github.com/click-contrib/click-option-group',
        "Issue tracker": 'https://github.com/click-contrib/click-option-group/issues',
        "Documentation": 'https://click-option-group.readthedocs.io',
    },
    license='BSD-3-Clause',
    author='Eugene Prilepin',
    author_email='esp.home@gmail.com',
    description='Option groups missing in Click',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
