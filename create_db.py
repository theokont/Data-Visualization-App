
import sqlite3
import os

# Create a database only if one does not exist


class create_database:

    db_filename = "sensor_data.db"

    def __init__(self):

        self.db_exists = not os.path.exists(self.db_filename)

        if self.db_exists:
            self.conn = sqlite3.connect(self.db_filename)
            self.conn.commit()
            self.conn.close()
            print('Database created.')
        else:
            print('Database already exists.')


class create_table:
    db_filename = "sensor_data.db"

    def __init__(self, sensor_name):

        self.conn = sqlite3.connect(self.db_filename)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS %s (
                            UNIT real,
                            VALUE real,
                            timedate text
                            )""" % (sensor_name,))
        self.conn.commit()
        self.conn.close()


table_name = input("Please enter the table name: ")

create_database()
create_table(table_name)
