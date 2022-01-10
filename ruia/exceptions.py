#!/usr/bin/env python


class IgnoreThisItem(Exception):
    """Ignore Ruia's Item"""

    pass


class InvalidCallbackResult(Exception):
    """Get an invalid callback result"""

    pass


class InvalidFuncType(Exception):
    """Get an invalid function type"""

    pass


class InvalidRequestMethod(Exception):
    """Get an invalid request method"""

    pass


class NotImplementedParseError(Exception):
    """Get an invalid callback result"""

    pass


class NothingMatchedError(Exception):
    """Target match error"""

    pass


class SpiderHookError(Exception):
    """Spider hook function execution error"""

    pass
