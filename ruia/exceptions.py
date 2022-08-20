"""
    Created by howie.hu at 2018.
    Description: Custom Exception for Ruia
    Changelog: all notable changes to this file will be documented
"""


class IgnoreThisItem(Exception):
    """Ignore Ruia's Item"""


class InvalidCallbackResult(Exception):
    """Get an invalid callback result"""


class InvalidFuncType(Exception):
    """Get an invalid function type"""


class InvalidRequestMethod(Exception):
    """Get an invalid request method"""


class NotImplementedParseError(Exception):
    """Get an invalid callback result"""


class NothingMatchedError(Exception):
    """Target match error"""


class SpiderHookError(Exception):
    """Spider hook function execution error"""
