import MySQLdb
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# CREDENTIALS
def get_credentials():
    USER = os.getenv('MYSQL_USER')
    PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')

    if not USER or not PASSWORD:
        raise ValueError('Database credentials are not set in enviroment variables')
    return USER, PASSWORD


# CLASS CREATE STRUCTURE IN DB USERS VALUES (FOR REGISTER AND AUTENTICATION)
class StructTableDbUsers():
    def __init__(self):
        self.host = "db_host"
        self.user, self.password = get_credentials()
        self.database = "db_electionxchain"

    def cnx(self):
        try:
            mydb = MySQLdb.connect(
                host = self.host,
                user = self.user,
                passwd = self.password,
                db = self.database
            )
            logger.info('Successful connection to the DB')
            return mydb
        except MySQLdb.Error as err:
            logger.error(f'Error: {err}')
            return None    
        
    def create_table(self):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    # Drop table if exists
                    cursor.execute("DROP TABLE IF EXISTS users;") 

                    # Create new table with the values of the register(form) and autentication(default)
                    cursor.execute("""CREATE TABLE users (
                        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        NIE VARCHAR(9) NOT NULL UNIQUE,
                        birth DATE NOT NULL,
                        province VARCHAR(50) NOT NULL,
                        genre VARCHAR(10),
                        number_tel VARCHAR(15) NOT NULL,
                        pub_key VARBINARY(500),
                        priv_key VARBINARY(500),
                        activate TINYINT(1)
                    );""")
                    
                    mydb.commit()
                    logger.info('Table created successfully')
            except MySQLdb.Error as err:
                logger.error(f"Error creating table: {err}")
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error(f"Connection to the database failed.")


# INSERT NEW DATA (REGISTER PART)
class InsertDataDbUsers():
    def __init__(self):
        self.host = "db_host"
        self.user, self.password = get_credentials()
        self.database = "db_electionxchain"

    def cnx(self):
        try:
            mydb = MySQLdb.connect(
                host = self.host,
                user = self.user,
                passwd = self.password,
                db = self.database
            )
            logger.info('Successful connection to the DB')
            return mydb
        except MySQLdb.Error as err:
            logger.error(f'Error: {err}')
            return None
        
    def insert_data_db(self, user_instance):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "INSERT INTO users (name, nie, birth, province, genre, number_tel, pub_key, priv_key, activate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    val = (
                        user_instance.name,
                        user_instance.nie,
                        user_instance.birth,
                        user_instance.province,
                        user_instance.genre,
                        user_instance.number_tel,
                        user_instance.pub_key,
                        user_instance.priv_key,
                        user_instance.activate
                    )

                    cursor.execute(sql, val)
                    mydb.commit()
                    logger.info('Data insert Successfully')
            except MySQLdb.Error as err:
                logger.error(f'Error to insert new data: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')
            sys.stdout.flush()


# CHECK IF NIE EXISTS FOR USER ALREADY REGISTERED
class ShowNieExists():
    def __init__(self):
        self.host = "db_host"
        self.user, self.password = get_credentials()
        self.database = "db_electionxchain"

    def cnx(self):
        try:
            mydb = MySQLdb.connect(
                host = self.host,
                user = self.user,
                passwd = self.password,
                db = self.database
            )
            logger.info('Successful connection to the DB')
            return mydb
        except MySQLdb.Error as err:
            logger.error(f'Error: {err}')
            return None
    
    def show_nie_exists(self, nie):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM users where NIE = %s"
                    cursor.execute(sql, (nie,))
                    result = cursor.fetchone()
                    exists = result[0]>0
                    logger.info(f'NIE check: {"Exists" if exists else "Does not exist"}')
                    return exists
            except MySQLdb.Error as err:
                logger.error(f'Error to fetching the NIE: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')
            sys.stdout.flush()


# CHECK IF NUMBER_TELEPHONE EXISTS FOR USER ALREADY REGISTERED
class ShowTelephoneExists():
    def __init__(self):
        self.host = "db_host"
        self.user, self.password = get_credentials()
        self.database = "db_electionxchain"

    def cnx(self):
        try:
            mydb = MySQLdb.connect(
                host = self.host,
                user = self.user,
                passwd = self.password,
                db = self.database
            )
            logger.info('Successful connection to the DB')
            return mydb
        except MySQLdb.Error as err:
            logger.error(f'Error: {err}')
            return None
    
    def show_telephone_exists(self, number):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM users where number_tel = %s"
                    cursor.execute(sql, (number,))
                    result = cursor.fetchone()
                    exists = result[0]>0
                    logger.info(f'Telephone Number check: {"Exists" if exists else "Does not exist"}')
                    return exists
            except MySQLdb.Error as err:
                logger.error(f'Error to fetching the Telephone number: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')
            sys.stdout.flush()