from typing import Optional

from database_utils import DatabaseUtils
from account import Account


class NightclubDatabaseAPI:
    def __init__(
            self,
            reinitialize_schema: Optional[bool] = False
    ) -> None:
        self.db_utils = DatabaseUtils()

        if reinitialize_schema:
            self.db_utils.init_schema()

        self.account = Account(
            db_utils=self.db_utils
        )
