#!/usr/bin/env python

from .field import AttrField, BaseField, ElementField, HtmlField, RegexField, TextField
from .item import Item
from .middleware import Middleware
from .request import Request
from .response import Response
from .spider import Spider
from .exceptions import IgnoreThisItem

__version__ = "0.6.7"
