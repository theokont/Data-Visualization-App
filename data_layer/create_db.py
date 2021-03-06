
import sqlite3

"""" DatabaseInteraction class that creates a DatabaseInteraction and has the basic query methods """


class DatabaseInteraction:

    def __init__(self, db_name):
        self.name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        # print('DatabaseInteraction {} has been created'.format(db_name))

    def create_table(self, table_name):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS %s (
                            UNIT text,
                            VALUE real,
                            TIME text
                            )""" % table_name)
        self.conn.commit()

    def drop_table(self, table_name):
        self.cur.execute("""DROP TABLE %s""" % table_name)
        self.conn.commit()

    def insert_values(self, db_table, values):
        self.cur.execute("INSERT INTO %s VALUES (?, ?, ?)" % db_table, (values))
        self.conn.commit()

    def select_all(self):
        self.cur.execute("SELECT * FROM sensor")
        return self.cur.fetchall()

    def select_values(self, select_string):
        self.cur.execute(select_string)
        return self.cur.fetchall()

    def clear_table(self):
        self.cur.execute("""DELETE FROM sensor""")
        self.conn.commit()
