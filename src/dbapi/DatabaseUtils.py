import psycopg2
import yaml
import os


class DatabaseUtils:
    def __init__(
            self,
            db_credentials: str = '../../../config/db.yml'
    ) -> None:
        """
        Store database credentials in memory to prevent file parsing for each query
        :param db_credentials:
        """
        yml_path = os.path.join(os.path.dirname(__file__), db_credentials)

        with open(yml_path, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.db_credentials = dict(
            dbname=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )

    def connect(self) -> psycopg2.connect:
        """
        Create a database connection.
        :return: psycopg connection
        """
        return psycopg2.connect(
            dbname=self.db_credentials['database'],
            user=self.db_credentials['user'],
            password=self.db_credentials['password'],
            host=self.db_credentials['host'],
            port=self.db_credentials['port']
        )

    def init_schema(
            self,
            schema_path: str = 'schema.sql'
    ) -> None:
        """
        Recreate the tables to initialize the db.
        :return: None
        """
        self.exec_sql_file(schema_path)

    def get_all_rows(
            self,
            table_name: str
    ) -> list[tuple]:
        """
        Get all rows from a table.
        :param table_name: a name of table
        :return: a list of tuples in the format
            [(col1_row1_value, col2_row1_value, ...,), (col2_row1_value, col2_row2_value, ...,),]
        """
        return self.exec_get_all(f'SELECT * FROM {table_name}')

    def update_partial(
            self,
            uuid: str,
            table_name: str,
            fields: dict
    ) -> None:
        """
        Update field values of the passed fields in a specified table.
        :param uuid: id of a table record
        :param table_name: name of the table
        :param fields: dict with arguments to update
        :return: None
        """

        for item in list(fields.items())[2:]:   # iterate through caller func args except [self, uuid
            if item[1]:                         # if arg was passed update it
                sql = f'''
                    UPDATE {table_name} SET {item[0]} = '{item[1]}' WHERE uuid = '{uuid}'
                '''
                self.exec_commit(sql)

    def exec_sql_file(
            self,
            path: str
    ) -> None:

        full_path = os.path.join(os.path.dirname(__file__), f'../{path}')
        conn = self.connect()
        cur = conn.cursor()

        with open(full_path, 'r') as file:
            cur.execute(file.read())

        conn.commit()
        conn.close()

    def exec_get_one(
            self,
            sql: str,
            args=None
    ) -> tuple:
        if args is None:
            args = {}

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, args)
        one = cur.fetchone()

        conn.close()

        return one

    def exec_get_all(
            self,
            sql: str,
            args=None
    ) -> list[tuple]:

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, args)
        # https://www.psycopg.org/docs/cursor.html#cursor.fetchall
        list_of_tuples = cur.fetchall()

        conn.close()

        return list_of_tuples

    def exec_commit(
            self,
            sql,
            args=None
    ) -> tuple:

        conn = self.connect()
        cur = conn.cursor()
        result = cur.execute(sql, args)
        conn.commit()

        conn.close()

        return result
