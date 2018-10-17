#!/usr/bin/env python

import logging


def get_logger(name='Ruia'):
    logging_format = "[%(asctime)s]-%(name)s-%(levelname)-6s"
    # logging_format += "%(module)-7s::l%(lineno)d: "
    logging_format += "%(module)-7s: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format,
        level=logging.DEBUG
    )
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("pyppeteer").setLevel(logging.INFO)
    logging.getLogger("websockets").setLevel(logging.INFO)
    return logging.getLogger(name)
