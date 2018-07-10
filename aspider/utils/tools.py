#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/9.
"""
import os
import random

import aiofiles


async def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    return random.choice(await _get_data('./user_agents.txt', USER_AGENT))


async def _get_data(filename: str, default: str = "hello") -> list:
    """
    Get data from all user_agents
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(root_folder, filename)
    try:
        async with aiofiles.open(user_agents_file, mode='r') as f:
            data = [_.strip() for _ in await f.readlines()]
    except:
        data = [default]
    return data


if __name__ == '__main__':
    import asyncio

    result = asyncio.get_event_loop().run_until_complete(get_random_user_agent())
    print(result)
