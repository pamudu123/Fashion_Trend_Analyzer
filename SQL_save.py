import mysql.connector
import json
import args


class SQLManager:
    def __init__(self):
        self.db = mysql.connector.connect(
            host = args.HOST,
            user = args.SQL_USERNAME,
            passwd = args.SQL_PASSWORD,
            database = args.SQL_DATABASE_NAME
        )

        self.cursor = self.db.cursor()
    
    def create_table_if_not_exists(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS TrackRecords (
            itn INT,
            date DATE,
            time TIME,
            age VARCHAR(255),
            gender VARCHAR(255),
            upper_color VARCHAR(255),
            bottom_color VARCHAR(255)
        )
        """
        self.cursor.execute(create_table_query)
        self.db.commit()
    
    def insert_record(self, itn, date, time, age, gender, upper_color, bottom_color):
        insert_query = """
        INSERT INTO TrackRecords (itn, date, time, age, gender, upper_color, bottom_color)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        age_str  = ','.join(map(str, age))
        values = (itn, date, time, age_str, gender, str(upper_color), str(bottom_color))
        self.cursor.execute(insert_query, values)
        self.db.commit()

    def close_connection(self):
        self.cursor.close()
        self.db.close()

if __name__ == "__main__":

    sql_manager = SQLManager()
    sql_manager.create_table_if_not_exists()

    # Example record
    itn = 2
    date = "2023-10-20"
    time = "15:30:00"
    age = (15,25)
    gender = "Male"
    upper_color = ('Red', 78)
    bottom_color = ('Blue', 63)

    sql_manager.insert_record(itn, date, time, age, gender, upper_color, bottom_color)

    # Close the database connection when done
    sql_manager.close_connection()


# View values form SQL Workbench
# SELECT * FROM TrackRecords;
