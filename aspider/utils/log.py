#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/9.
"""
import logging


def get_logger(name='aspider'):
    logging_format = "[%(asctime)s]-%(name)s-%(levelname)-6s"
    # logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format,
        level=logging.DEBUG
    )
    logging.getLogger("asyncio").setLevel(logging.INFO)
    return logging.getLogger(name)

