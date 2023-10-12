from flask import Flask
from flask_restful import Resource, Api

from api.management import *
from api.account import Account
from api.login import Login

from dbapi.nightclub_database_api import NightclubDatabaseAPI


nightclub_dbapi = NightclubDatabaseAPI(reinitialize_schema=False)

app = Flask(__name__)
api = Api(app)

# Management API for initializing the DB
api.add_resource(
    Init,
    '/manage/init',
    resource_class_kwargs={'dbapi': nightclub_dbapi}
)

# Get full Account info or create Account
api.add_resource(
    Account,
    '/accounts/<string:account_id>',    # get full Account info
    '/accounts/create',                 # create Account
    resource_class_kwargs={'dbapi': nightclub_dbapi}
)

# Authenticate user
api.add_resource(
    Login,
    '/login/<string:account_id>'    # authenticate user
)


if __name__ == '__main__':
    app.run(debug=True, port=4999)
