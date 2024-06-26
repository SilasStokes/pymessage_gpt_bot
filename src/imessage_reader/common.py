#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
common.py
Python 3.8+
Date created: June 14th, 2020
Date modified: February 26th, 2022
"""

import platform
import sqlite3
from enum import Enum

VERSION = "0.4.0"


class Platform(Enum):
    """
    An enum used to indicate the system's operating system
    """

    OTHER = 0
    LINUX = 1
    MAC = 2
    WINDOWS = 3


def get_platform() -> str:
    """
    Get the current operating system.
    :return: The operating system this program is running on
    """

    system = platform.system()
    if system == "Linux":
        return str(Platform.LINUX.name)
    if system == "Darwin":
        return str(Platform.MAC.name)
    if system == "Windows":
        return str(Platform.WINDOWS.name)
    raise NotImplementedError(f"Platform {system} is not supported yet!")


def fetch_db_data(db, command) -> list:
    """
    Send queries to the sqlite database and return the results.
    :param db: The path to the database.
    :param command: The Sqlite command.
    :return: Data from the database
    """
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(command)
        return cur.fetchall()
    except Exception as e:
        raise e
