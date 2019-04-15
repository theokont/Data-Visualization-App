
import sqlite3
import os

# Create a database only if one does not exist


class Database:

    # db_filename = "sensor_data.db"

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        # print('Database {} has been created'.format(db_name))

    def create_table(self, table_name):

        self.cur.execute("""CREATE TABLE IF NOT EXISTS %s (
                            UNIT real,
                            VALUE real,
                            timedate text
                            )""" % table_name)
        self.conn.commit()

    def drop_table(self, table_name):
        self.cur.execute("""DROP TABLE %s""" % table_name)
        self.conn.commit()


db_name = "sensor_data.db"
table_name = input("Please enter the table name: ")

db = Database(db_name)
db.create_table(table_name)

db_del = input("please enter db_del :")
db.drop_table(db_del)
