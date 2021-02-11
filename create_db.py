import psycopg2


class DB(object):
    def open(self):
        hostname = '127.0.0.1'
        username = 'parsing_admin'
        password = 'parsing_adminparsing_admin'
        database = 'parsing'
        port = "5444"
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        self.cur = self.connection.cursor()

    def close(self):
        self.cur.close()
        self.connection.close()

    def drop_table(self):
        self.cur.execute(
            """DROP TABLE table_1"""
        )
        self.connection.commit()

    def create_tables(self):
        """create tables in the database if they are not contained"""

        self.cur.execute('''CREATE TABLE IF NOT EXISTS my_business_entry
                        (
                        id SERIAL PRIMARY KEY,
                        url_yes_no boolean,
                        url TEXT,
                        phone_yes_no boolean,
                        phone TEXT,
                        rating TEXT,
                        nr_of_ratings TEXT,
                        myBusiness boolean,
                        company TEXT
                        );''')

        self.connection.commit()


if __name__ == '__main__':
    db = DB()
    db.open()
    db.create_tables()
    db.close()
