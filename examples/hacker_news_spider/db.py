#!/usr/bin/env python
"""
 pip install motor
"""

import asyncio

from motor.motor_asyncio import AsyncIOMotorClient


class MotorBase:
    """
    About motor's doc: https://github.com/mongodb/motor
    """
    _db = {}
    _collection = {}

    def __init__(self, loop=None):
        self.motor_uri = ''
        self.loop = loop or asyncio.get_event_loop()

    def client(self, db):
        # motor
        self.motor_uri = f"mongodb://localhost:27017/{db}"
        return AsyncIOMotorClient(self.motor_uri, io_loop=self.loop)

    def get_db(self, db='test'):
        """
        Get a db instance
        :param db: database name
        :return: the motor db instance
        """
        if db not in self._db:
            self._db[db] = self.client(db)[db]

        return self._db[db]
