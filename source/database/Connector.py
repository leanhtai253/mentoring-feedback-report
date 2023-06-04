import psycopg2

class DatabaseConnector:
    def __init__(self, database, user, password, host, port=None):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        conn = psycopg2.connect(
            database=self.database, user=self.user, password=self.password, host=self.host, port=self.port
        )
        return conn