#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/9.
"""
import logging


def get_logger():
    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format,
        level=logging.DEBUG
    )
    return logging.getLogger('dc_async_spider')


logger = get_logger()
