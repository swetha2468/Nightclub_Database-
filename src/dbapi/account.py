import uuid

from typing import Any

from database_utils import DatabaseUtils

TABLE_NAME = 'account'


class Account:
    def __init__(
            self,
            db_utils: DatabaseUtils,
    ) -> None:
        self.db_utils = db_utils

    def create_one(
            self    # arguments can be added to create account with some more fields through _update_one()
    ) -> str:
        """
        Create an account. Creates empty account with UID only.
        :return: UID of a created account
        """

        db_uid = str(uuid.uuid4())  # create primary key here, so we don't need to fetch it from database after insert

        sql = f'''
                INSERT INTO {TABLE_NAME} (uid) VALUES  ('{db_uid}');
        '''
        self.db_utils.exec_commit(sql)

        return db_uid

    def _update_one(
            self,
            account_id: str,
    ) -> dict:
        """
        Update an account. All the arguments except account_id are optional,
        therefore only those passed will be updated for specified account.
        If nothing's passed nothing will be updated.
        :return: list with a tuple containing updated account rows
        """

        arg_dict = locals().copy()
        self.db_utils.update_partial(account_id, table_name='account', fields=arg_dict)

        return self.get_one(account_id)  # return all account fields of the updated account

    def get_one(
            self,
            account_id: str,
            *args
    ) -> Any:
        """
        Get all rows for a specific account record identified by UID
        :param account_id: account UID
        :param args: fields to fetch, if empty, all fields will be fetched
        :return: dict of fields in the following format:
            {'account_id': '123-456', ...}
        """

        sql = f'''
            SELECT * FROM {TABLE_NAME} WHERE uuid = '{account_id}'
        '''
        result = self.db_utils.exec_get_one(sql)

        return dict(
            account_id=result[0],   # return python dict with all account rows. result contains list of table rows

        ) if result else None
