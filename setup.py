#!/usr/bin/env python

import os
import re
import sys

from setuptools import find_packages, setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

PY_VER = sys.version_info

if PY_VER < (3, 6):
    raise RuntimeError("ruia doesn't support Python version prior 3.6")


def read_version():
    regexp = re.compile(r'^__version__\W*=\W*"([\d.abrc]+)"')
    init_py = os.path.join(os.path.dirname(__file__), "ruia", "__init__.py")
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name="ruia",
    version=read_version(),
    author="Howie Hu",
    description="Async Python 3.6+ web scraping micro-framework based on asyncio.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author_email="xiaozizayang@gmail.com",
    python_requires=">=3.6",
    install_requires=["aiohttp>=3.5.4", "cssselect", "lxml"],
    url="https://python-ruia.org/",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: BSD",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Documentation": "https://docs.python-ruia.org/",
        "Source": "https://github.com/howie6879/ruia",
    },
    extras_require={"uvloop": ["uvloop"]},
)
