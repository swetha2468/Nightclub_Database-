from flask_restful import Resource, reqparse, request  # NOTE: Import from flask_restful, not python


class Init(Resource):
    def __init__(self, dbapi):
        self.dbapi = dbapi

    def post(self):
        self.dbapi.db_service.init_schema()
        return 200


class Version(Resource):
    def __init__(self, dbapi):
        self.dbapi = dbapi

    def get(self):
        return self.dbapi.db_service.exec_get_one('SELECT VERSION()')