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


# CLASS CREATE STRUCTURE IN DB
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
                        id VARCHAR(36) DEFAULT(uuid()) PRIMARY KEY NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        dni VARCHAR(9) NOT NULL UNIQUE,
                        birth DATE NOT NULL,
                        province VARCHAR(50) NOT NULL,
                        genre VARCHAR(10),
                        number_tel VARCHAR(15) NOT NULL,
                        pub_key VARBINARY(500),
                        priv_key VARBINARY(500),
                        regist_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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


# INSERT
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
                    sql = "INSERT INTO users (name, dni, birth, province, genre, number_tel, pub_key, priv_key, activate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    val = (
                        user_instance.name,
                        user_instance.dni,
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


# SELECT
class ShowsDataDbUsers():
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
    
    # CHECK IF NIE EXISTS FOR USER ALREADY REGISTERED
    def show_dni_exists(self, dni):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM users where dni = %s"
                    cursor.execute(sql, (dni,))
                    result = cursor.fetchone()
                    exists = result[0]>0
                    logger.info(f'DNI check: {"Exists" if exists else "Does not exist"}')
                    return exists
            except MySQLdb.Error as err:
                logger.error(f'Error to fetching the DNI: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')
    
    # CHECK IF NUMBER_TELEPHONE EXISTS FOR USER ALREADY REGISTERED
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
    
    # VALIDATE THE DNI/NIE WITH THE TELEPHONE NUMBER
    def show_dni_tel_exists_for_a_user(self, dni, number_tel):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM users where dni = %s and number_tel = %s"
                    cursor.execute(sql, (dni,number_tel,))
                    result = cursor.fetchone()
                    exists = result[0]>0
                    logger.info(f'User exists for that dni and tel_number: {"Exists" if exists else "Does not exist"}')
                    return exists
            except MySQLdb.Error as err:
                logger.error(f'Error to fetching the user data for validation: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')

    # FETCH ID FOR A GIVEN DNI/NIE
    def show_id_user(self, dni):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT id FROM users where dni = %s"
                    cursor.execute(sql, (dni,))
                    result = cursor.fetchone()
                    if result is None:
                        logger.error('Error: Failed to try fetch the id.')
                        return
                    logger.info(f'Successfully fetching the id')
                    return result[0]
            except MySQLdb.Error as err:
                logger.error(f'Error to fetching the id: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')

    # FETCH TELEPHONE NUMBER FOR A GIVEN ID 
    def show_numberTel_user(self, id):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT number_tel FROM users where id = %s"
                    cursor.execute(sql, (id,))
                    result = cursor.fetchone()
                    if result:
                        number_tel = result[0]
                        logger.info(f'Successfully fetched number_tel: {number_tel}')
                        return number_tel
                    else:
                        logger.error(f'Error: No number_tel found for ID {id}')
                        return None
            except MySQLdb.Error as err:
                logger.error(f'Error to fetching the number_tel: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')

    
    