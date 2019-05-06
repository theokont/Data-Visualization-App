
import sqlite3
import os

"""" Database class that creates a database and has the basic query methods """


class Database:

    # db_filename = "sensor_data.db"

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        # print('Database {} has been created'.format(db_name))

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
        # % db_table % one % two)
        # tha kanw preparedstatements kai tha kanw bind to argument
        # (dld tha exw ena string pou tha to vazw san input edw)
        # self.cur.execute(prepared_statement)
        self.cur.execute("SELECT * FROM sensor")
        return self.cur.fetchall()
        self.con.commit()

    def select_values(self, select_string):
        self.cur.execute(select_string)
        return self.cur.fetchall()
        self.con.commit()

    def clear_table(self, table_name):
        self.cur.execute("""DELETE FROM %s""" % table_name)
        self.conn.commit()


if __name__ == '__main__':
    db_name = "sensor_data.db"
    # table_name = input("Please enter the table name: ")

    db = Database(db_name)
    db_table = "sensor"
    db.create_table(db_table)
    # plot_list = db.select_values(db_table, "TIME", values[2])
    # print(plot_list)
    # db.drop_table(db_table)

    # db.insert_values(db_table, values)
    # db_del = input("please enter db_del :")
