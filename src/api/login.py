from typing import Tuple, Dict, Any
from flask_restful import Resource, fields, marshal_with

from auth_service import AuthenticationService
from dbapi.nightclub_database_api import NightclubDatabaseAPI


class Login(Resource):
    def __init__(self):
        self.auth_service = AuthenticationService(
            dbapi=NightclubDatabaseAPI
        )

    def get(
            self,
            account_id: str  # probably switch to user email
    ):
        is_authenticated = self.auth_service.check_credentials(account_id=account_id)

        pass
