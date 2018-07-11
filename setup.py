#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='aspider',
    version='0.0.1',
    author='Howie Hu',
    description="A lightweight,asynchronous,distributed scraping micro-framework",
    author_email='xiaozizayang@gmail.com',
    install_requires=['aiofiles', 'aiohttp', 'cchardet', 'cssselect', 'lxml'],
    url="https://github.com/howie6879/aspider/blob/master/README.md",
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    package_data={'aspider': ['utils/*.txt']})
