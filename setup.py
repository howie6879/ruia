#!/usr/bin/env python
import os

from setuptools import find_packages, setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='aspider',
    version='0.0.2',
    author='Howie Hu',
    description="A lightweight,asynchronous,distributed scraping micro-framework",
    long_description=read('README.md'),
    author_email='xiaozizayang@gmail.com',
    install_requires=['aiofiles', 'aiohttp', 'cchardet', 'cssselect', 'lxml'],
    url="https://github.com/howie6879/aspider/blob/master/README.md",
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
        'Documentation': 'https://github.com/howie6879/aspider',
        'Source': 'https://github.com/howie6879/aspider',
    },
    package_data={'aspider': ['utils/*.txt']})
