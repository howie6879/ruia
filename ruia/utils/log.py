"""
    Created by howie.hu at 2022-08-21.
    Description: Get logger
    Changelog: all notable changes to this file will be documented
"""

import logging


def get_logger(name="Ruia"):
    """
    Get logger
    Args:
        name (str, optional): logger name. Defaults to "Ruia".

    Returns:
        _type_: Logger
    """
    logging_format = f"[%(asctime)s] %(levelname)-5s %(name)-{len(name)}s "
    # logging_format += "%(module)-7s::l%(lineno)d: "
    # logging_format += "%(module)-7s: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format, level=logging.INFO, datefmt="%Y:%m:%d %H:%M:%S"
    )
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("websockets").setLevel(logging.INFO)
    return logging.getLogger(name)
