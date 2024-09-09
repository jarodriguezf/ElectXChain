import MySQLdb
import os
import sys
import logging
import hashlib

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


# TABLE
class CreateTableCounter():
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
                    # DROP TABLE IF EXISTS
                    cursor.execute("DROP TABLE IF EXISTS counter;") 

                    cursor.execute("""CREATE TABLE counter (
                        vote VARCHAR(7) NOT NULL,
                        count INT DEFAULT 0 NOT NULL
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


# COUNTING VOTE IF WE NEED TO UPDATE OR INSERT
class SaveNewVotesCount():
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


    # INSERT THE VOTES OR UPDATE IT
    def sendVoteToDB(self, vote_option, count):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    # CHECK IF VOTE EXISTS
                    cursor.execute("SELECT count FROM counter WHERE vote = %s", (vote_option,))
                    result = cursor.fetchone() 

                    if result:
                        # IF VOTE EXISTS, UPDATE THE COUNTER +1
                        cursor.execute("UPDATE counter SET count = count + %s WHERE vote = %s", (count, vote_option))
                    else:
                        # IF VOTE NOT EXISTS, INSERT THE NEW COUNT AND VOTE
                        cursor.execute("INSERT INTO counter (vote, count) VALUES (%s, %s)", (vote_option, count))
                
                    mydb.commit()
                    logger.info('Vote update successfully')
            except MySQLdb.Error as err:
                logger.error(f"Error updating vote count in database: {err}")
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error(f"Connection to the database failed.")


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
    
    # GET THE PUBLIC KEY OF THE USER
    def show_pub_key_user(self, id):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT pub_key FROM users where id = %s;"
                    cursor.execute(sql, (id,))
                    result = cursor.fetchone()
                    if result is None or len(result[0]) == 0:
                        logger.error(f'Error: Pub key not found for ID {id}')
                        return None
                    logger.info(f'Pub key found for ID: {id}')
                    return result[0]
            except MySQLdb.Error as err:
                logger.error(f'Error to find the Pub key: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')
    

    # GET THE VOTE HASH OF THE USER
    def show_votehashed_user(self, id):
        mydb = self.cnx()
        if mydb:
            try:
                with mydb.cursor() as cursor:
                    sql = "SELECT voted_hash FROM users where id = %s;"
                    cursor.execute(sql, (id,))
                    result = cursor.fetchone()
                    if result is None or len(result[0]) == 0:
                        logger.error(f'Error: Vote not found for ID {id}')
                        return None
                    logger.info(f'Vote found for ID: {id}')
                    return result[0]
            except MySQLdb.Error as err:
                logger.error(f'Error to find the Vote: {err}')
            finally:
                mydb.close()
                logger.info('Database connection closed')
        else:
            logger.error('Connection to the database failed.')