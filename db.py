import sqlite3

class DB:

    def __init__(self, db_file):
        self.connected = False
        self.connection = 0
        self.db_file = db_file

    def connect(self):
        if not self.connected:
            try:
                self.connection = sqlite3.connect(self.db_file)
                self.connected = True
            except Exception as e:
                print(e)

    def close(self):
        if self.connected:
            self.connection.commit()
            self.connection.close()
            self.connected = False

    def create_table(self, statement):
        self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(statement)
        except Exception as e:
            print(e)
        self.close()

    def insert_response(self, values):
        self.connect()
        statement = 'INSERT INTO Responses VALUES (?, ?, ?);'
        cursor = self.connection.cursor()
        try:
            cursor.execute(statement, values)
        except Exception as e:
            print(e)
        self.close()

    def select_all(self, table_name):
        self.connect()
        statement = "SELECT * FROM " + str(table_name) + ";"
        cursor = self.connection.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()
        self.close()
        return results
