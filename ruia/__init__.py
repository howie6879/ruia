"""
    Created by howie.hu at 2018.
    Description: Init Ruia
    Changelog: all notable changes to this file will be documented
"""


from .exceptions import IgnoreThisItem
from .field import AttrField, BaseField, ElementField, HtmlField, RegexField, TextField
from .item import Item
from .middleware import Middleware
from .request import Request
from .response import Response
from .spider import Spider

__version__ = "0.8.5"
