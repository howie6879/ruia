#!/usr/bin/env python
import os
import re

from setuptools import find_packages, setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'ruia/__init__.py')) as fp:
    try:
        version = re.findall(
            r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='ruia',
    version=version,
    author='Howie Hu',
    description="Ruia - An async web scraping micro-framework based on asyncio.",
    long_description=read('README.md'),
    author_email='xiaozizayang@gmail.com',
    install_requires=['aiohttp', 'cchardet', 'cssselect', 'lxml', 'pyppeteer'],
    url="https://github.com/howie6879/ruia/blob/master/README.md",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Documentation': 'https://github.com/howie6879/ruia',
        'Source': 'https://github.com/howie6879/ruia',
    },
    extras_require={
        'uvloop': ['uvloop']
    }
)
