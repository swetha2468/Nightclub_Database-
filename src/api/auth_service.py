

class AuthenticationService:
    def __init__(
            self,
            dbapi
    ) -> None:
        self.dbapi = dbapi

    def check_credentials(self, account_id):
        pass
