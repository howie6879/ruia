#!/usr/bin/env python
"""
    Created by howie.hu at 12/27/20.
    Copyright (c) 2013-present, Xiamen Dianchu Technology Co.,Ltd.
    Description:
    Changelog: all notable changes to this file will be documented
"""

import json
import os
from pathlib import Path
from typing import List

import aiofiles
from ruia import Item, Spider, TextField


def mkdirs_if_not_exist(dir):
    """文件夹不存在时则创建。
    :param str dir: 文件夹路径，支持多级
    """
    if not os.path.isdir(dir):
        try:
            os.makedirs(dir)
            return True
        except FileExistsError:
            pass


def safe_filename(filename):
    """去掉文件名中的非法字符。
    :param str filename: 文件名
    :return str: 合法文件名
    """
    return "".join([c for c in filename if c not in r'\/:*?"<>|']).strip()


IMAGE_HOST = "http://imgoss.cnu.cc/"
BASE_DIR = "www.cnu.cc"
THUMBNAIL_PARAMS = "?x-oss-process=style/content"

APP_NAME = "CNU Scraper"
START_URLS = ["http://www.cnu.cc/works/{work_id}"]
DESTINATION = Path(".")
CONCURRENCY = 30
OVERWRITE = False
RETRIES = 3
TIMEOUT = 30.0
THUMBNAIL = False


class CNUItem(Item):
    target_item = TextField(css_select="body")
    title = TextField(css_select=".work-title")
    imgs_json = TextField(css_select="#imgs_json")


class CNUSpider(Spider):
    name = APP_NAME
    start_urls = START_URLS
    request_config = {"RETRIES": RETRIES, "DELAY": 0, "TIMEOUT": TIMEOUT}
    concurrency = CONCURRENCY
    # aiohttp config
    aiohttp_kwargs = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._destination = DESTINATION
        self._overwrite = OVERWRITE
        self._thumbnail = THUMBNAIL
        # 更新 Spider 及自定义的配置
        for k, v in kwargs.get("spider_config", {}).items():
            setattr(self, k, v)

    async def parse(self, response):
        async for item in CNUItem.get_items(html=await response.text()):
            urls = [IMAGE_HOST + img.get("img") for img in json.loads(item.imgs_json)]
            for index, url in enumerate(urls):
                basename = url.split("/")[-1]
                save_dir = self._destination / BASE_DIR / safe_filename(item.title)
                fpath = save_dir / f"[{index + 1:02d}]{basename}"
                if self._overwrite or not fpath.is_file():
                    if self._thumbnail:
                        url += THUMBNAIL_PARAMS
                    self.logger.info(f"Downloading {url} ...")
                    yield self.request(
                        url=url,
                        metadata={
                            "title": item.title,
                            "index": index,
                            "url": url,
                            "basename": basename,
                            "save_dir": save_dir,
                            "fpath": fpath,
                        },
                        callback=self.save_image,
                    )
                else:
                    self.logger.info(f"Skipped already exists: {fpath}")

    async def process_item(self, item):
        pass

    async def save_image(self, response):
        # 创建图片保存目录
        save_dir = response.metadata["save_dir"]
        if mkdirs_if_not_exist(save_dir):
            self.logger.info(f"Created directory: {save_dir}")
        # 保存图片
        fpath = response.metadata["fpath"]
        try:
            content = await response.read()
        except TypeError as e:
            self.logger.error(e)
        else:
            async with aiofiles.open(fpath, "wb") as f:
                await f.write(content)
                self.logger.info(f"Saved to {fpath}")


if __name__ == "__main__":
    # 开始爬虫任务
    CNUSpider.start(
        spider_config=dict(
            start_urls=list(["http://www.cnu.cc/works/427334"]),
            request_config={"RETRIES": RETRIES, "DELAY": 1, "TIMEOUT": TIMEOUT},
            _destination=DESTINATION,
            _overwrite=OVERWRITE,
            _thumbnail=CONCURRENCY,
            concurrency=THUMBNAIL,
        )
    )
