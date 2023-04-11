#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch data, print data and export data to excel.
Python 3.8+
Author: niftycode
Modified by: thecircleisround
Date created: October 8th, 2020
Date modified: February 19th, 2022
"""

import sys

from os.path import expanduser

from imessage_reader import common, create_sqlite, write_excel, data_container


# noinspection PyMethodMayBeStatic
class FetchData:
    """
    This class contains the methods to fetch, print and export the messages.
    """

    # The path to the iMessage database
    DB_PATH = expanduser("~") + "/Library/Messages/chat.db"

    # The SQL command
    SQL_CMD = (
        "SELECT "
            "text, "
            "datetime((date / 1000000000) + 978307200, 'unixepoch', 'localtime'),"
            "handle.id, "
            "handle.service, "
            "message.destination_caller_id, "
            "message.is_from_me, "
            "message.attributedBody, "
            "message.cache_roomnames, "
            "chat.display_name "
        "FROM "
            "message "
        "LEFT JOIN "
            "handle on message.handle_id=handle.ROWID "
        "LEFT JOIN "
            "chat ON message.cache_roomnames=chat.chat_identifier "
    )

    def __init__(self, system=None):
        if system is None:
            self.operating_system = common.get_platform()

    def _check_system(self):
        if self.operating_system != "MAC":
            sys.exit("Your operating system is not supported yet!")

    def _read_database(self, sql_cmd:str = SQL_CMD) -> list[data_container.MessageData]:
        """
        Fetch data from the database and store the data in a list.
        :return: List containing the user id, messages, the service and the account
        """

        rval = common.fetch_db_data(self.DB_PATH, sql_cmd)
        # rval indices
        # 0. text message
        # 1. date
        # 2. phone_number/handle_id
        # 3. handle_service
        # 4. destination caller id
        # 5. message from me as 1 = from me, 0 = no
        # 6. attributedBody (contains text if index 0 is null)
        # 7. cache roomnames - groupchat identifier
        # 8. group chat display name

        data = []
        for row in rval:
            text = row[0]
            # the chatdb has some weird behavior where sometimes the text value is None
            # and the text string is buried in an binary blob under the attributedBody field.
            if text is None and row[6] is not None:
                try:
                    text = row[6].split(b'NSString')[1]
                    text = text[5:] # stripping some preamble which generally looks like this: b'\x01\x94\x84\x01+'
                    
                    if text[0] == 129: # this 129 is b'\x81, python indexes byte strings as ints, this is equivalent to text[0:1] == b'\x81'
                        length = int.from_bytes(text[1:3], 'little') 
                        text = text[3:length  + 3]
                    else:
                        length = text[0]
                        text = text[1:length + 1]
                    text = text.decode()
                except Exception as e:
                    pass
                    
            recipient = row[2] if not row[8] else row[8]

            data.append(
                data_container.MessageData(
                    recipient, text, row[1], row[3], row[4], row[5]
                )
            )

        return data

    def show_user_txt(self, export: str):
        """
        Invoke _read_database(), print fetched data and export data.
        This method is for CLI usage.
        :param export: Determine whether to export data
        """

        # Check the running operating system
        self._check_system()

        # Read chat.db
        fetched_data = self._read_database()

        # CLI output
        if export == "nothing":
            for data in fetched_data:
                print(data)

        # Excel export
        if export == "excel":
            self._export_excel(fetched_data)

        # SQLite3 export
        if export == "sqlite":
            self._export_sqlite(fetched_data)

        if export == "recipients":
            self._get_recipients()

    def _export_excel(self, data: list):
        """
        Export data (write Excel file)
        :param data: message objects containing user id, message, date, service, account
        """
        file_path = expanduser("~") + "/Desktop/"
        ew = write_excel.ExelWriter(data, file_path)
        ew.write_data()

    def _export_sqlite(self, data: list):
        """
        Export data (create SQLite3 database)
        :param data: message objects containig user id, message, date, service, account
        """
        file_path = expanduser("~") + "/Desktop/"
        cd = create_sqlite.CreateDatabase(data, file_path)
        cd.create_sqlite_db()

    def _get_recipients(self):
        """
        Create a list containing all recipients and
        show the recipients in the command line.
        """
        fetched_data = self._read_database()

        # Create a list with recipients
        recipients = [i.user_id for i in fetched_data if i.is_from_me == 0]

        print()
        print("List of Recipients")
        print("------------------------")
        print()

        for recipient in recipients:
            print(recipient)

    def get_messages(self) -> list:
        """
        Create a list with tuples (user id, message, date, service, account, is_from_me)
        This method is for module usage.
        :return: List with tuples (user id, message, date, service, account, is_from_me)
        """
        fetched_data = self._read_database()

        users = []
        messages = []
        dates = []
        service = []
        account = []
        is_from_me = []

        for data in fetched_data:
            users.append(data.user_id)
            messages.append(data.text)
            dates.append(data.date)
            service.append(data.service)
            account.append(data.account)
            is_from_me.append(data.is_from_me)

        data = list(zip(users, messages, dates, service, account, is_from_me))

        return data

    def get_most_recent_messages(self, x:int = 10) -> list[data_container.MessageData]:
        """
        return the x most recent texts from the database
        :accepts: an integer that represents how many texts should be retrieved. 
        :returns: list[data_container.MessageData] of length x that are in order from newest to oldest 
        """
        sql_query = self.SQL_CMD + (
            "ORDER BY "
                "message.date DESC "
            "LIMIT " + str(x) + " "
            ";"
        )
        return self._read_database(sql_query)

    def get_messages_from(self, contact_id:str = '+12223334444', num_records: int = -1) -> list[data_container.MessageData]:
        sql_query = self.SQL_CMD + (
            "WHERE "
                f"handle.id = \"{contact_id}\" "
                "OR "
                f"message.cache_roomnames = \"{contact_id}\" "
                "OR "
                f"chat.display_name = \"{contact_id}\" "
            "ORDER BY "
                "message.date DESC "
        )
        if num_records != -1:
            sql_query = sql_query + f'LIMIT {num_records};'
        else:
            sql_query = sql_query + ";"

        return self._read_database(sql_query)
    
    def get_messages_between_dates(self, date_start = None, date_end = None) -> list[data_container.MessageData]:
        """
        Dateformat should be: YYYY-MM-DD HH:MM:SS format, which can be done with the code::

            time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        and offset with::

            offset = 60 * 60 * 24 * 365 # SECONDS * MINUTES * HOURS * DAYS * YEARS
            time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - OFFSET))

        if date_end is not supplied, it will be assumed to be current time.
        If not returning anything, and you suspect it should be, ensure that you dont have start and end flopped. 
        :return:
        """ 
        from time import strftime, localtime, time, strptime

        if date_start is None:
            return None

        try:
            _ = strptime(date_start, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise e


        try:
            _ = strptime(date_end, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date_end = strftime('%Y-%m-%d %H:%M:%S',localtime(time())) # date end getting set to current time

        sql_query = self.SQL_CMD + (
            "WHERE "
                "DATETIME((message.date / 1000000000) + 978307200, 'unixepoch', 'localtime') "
                "BETWEEN "
                    f"\"{date_start}\" "
                "AND "
                    f"\"{date_end}\" "
            "ORDER BY "
                "message.date DESC "
            ";"
        )

        return self._read_database(sql_query)

    def get_messages_between_dates_from(self, contact_id: str = '', date_start:str = None, date_end:str = None) -> list[data_container.MessageData]:
        """
        Dateformat should be: YYYY-MM-DD HH:MM:SS format, which can be done with the code::

            time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        and offset with::

            offset = 60 * 60 * 24 * 365 # SECONDS * MINUTES * HOURS * DAYS * YEARS
            time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() - OFFSET))

        if date_end is not supplied, it will be assumed to be current time.
        If not returning anything, and you suspect it should be, ensure that you dont have start and end flopped. 
        :return:
        """ 
        from time import strftime, localtime, time, strptime

        if date_start is None:
            return None

        try:
            _ = strptime(date_start, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            raise e

        try:
            _ = strptime(date_end, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date_end = strftime('%Y-%m-%d %H:%M:%S',localtime(time())) # date end getting set to current time


        sql_query = self.SQL_CMD + (
            "WHERE "
                "DATETIME((message.date / 1000000000) + 978307200, 'unixepoch', 'localtime') "
                "BETWEEN "
                    f"\"{date_start}\" "
                "AND "
                    f"\"{date_end}\" "
                "AND "
                "( "
                    f"handle.id = \"{contact_id}\" "
                    "OR "
                    f"message.cache_roomnames = \"{contact_id}\" "
                    "OR "
                    f"chat.display_name = \"{contact_id}\" "
                ") "
            "ORDER BY "
                "message.date DESC "
            ";"
        )

        return self._read_database(sql_query)