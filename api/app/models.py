import MySQLdb
import os

USER = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')

# CLASS CREATE STRUCTURE IN DB USERS VALUES (FOR REGISTER AND AUTENTICATION)
class StructTableDbUsers():
    def __init__(self):
        self.host = "db_host"
        self.user = USER
        self.password = PASSWORD
        self.database = "db_electionxchain"
    
    def cnx(self):
        try:
            mydb = MySQLdb.connect(
            host = self.host,
            user = self.user,
            passwd = self.password,
            db = self.database
            )
            print("Successful connection to the DB")
            return mydb
        except MySQLdb.Error as err:
            print(f"Error: {err}")
            return None
        
        
    def create_table(self):
        mydb = self.cnx()
        if mydb:
            cursor = mydb.cursor()
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
            cursor.close()
            mydb.close()
        else:
            print("Connection to the database failed.")


class User():
    def __init__(self, name, nie, birth, province, genre, number_tel):
        self.name = name
        self.nie = nie
        self.birth = birth
        self.province = province
        self.genre =  genre
        self.number_tel = number_tel

    def get_user(self):
        return f"User(name={self.name}, nie={self.nie}, birth={self.birth}, province={self.province}, genre={self.genre}, number_tel={self.number_tel})"
    