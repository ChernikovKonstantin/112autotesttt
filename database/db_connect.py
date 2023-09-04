import psycopg2

from utils.base_util import BaseUtil


class DBConnect(BaseUtil):

    def __init__(self, config):
        self.config = config
        self._connection = None
        self._connect()

    def _connect(self):
        self._connection = psycopg2.connect(dbname=self.config.DB_NAME,
                                            user=self.config.DB_USER,
                                            password=self.config.DB_PASSWORD,
                                            host=self.config.DB_HOST,
                                            port=self.config.DB_PORT
                                            )
        self._connection.autocommit = True

    def _get_cursor(self):
        return self._connection.cursor()

    def select(self, query, args=None):
        cursor = self._execute(query, args)
        return cursor.fetchall()

    def delete(self, query, args=None):
        cursor = self._execute(query, args)
        return cursor.rowcount

    def update(self, query, args=None):
        cursor = self._execute(query, args)
        return cursor.statusmessage

    def insert(self, query, args=None):
        cursor = self._execute(query, args)
        return cursor.lastrowid

    def _execute(self, query, args=None):
        """
        :param query:
        :param args: parameters used with query. (optional)
        :type args: tuple, list or dict
        If args is a list or tuple, %s can be used as a placeholder in the query.
        If args is a dict, %(name)s can be used as a placeholder in the query.
        """
        import re
        cursor = self._get_cursor()
        cursor.execute(query, vars=args)
        cursor_query = re.sub(r'\n\s+', ' ', cursor.query.decode('utf-8'))
        log_message = f'query: "{cursor_query}"\nresult: {cursor.statusmessage}'
        self.xprint(log_message, allure_title='Sql query')
        return cursor

    def close(self):
        cursor = self._get_cursor()
        cursor.close()
        self._connection.close()


if __name__ == "__main__":
    pass
