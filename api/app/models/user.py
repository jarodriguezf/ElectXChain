from datetime import date
from typing import Optional
from pydantic import BaseModel


#USER STRUCTURE (2FA)
class PhoneNumberSchema(BaseModel):
    number_tel: int


#USER STRUCTURE (AUTENTICATION)
class UserAutSchema(BaseModel):
    dni: str
    number_tel: int

# USER CLASS AND STRUCTURE (REGISTER)
class UserSchema(BaseModel):
    name: str
    dni: str
    birth: date
    province: str
    genre: Optional[str] = None
    number_tel: int
    pub_key: Optional[bytes] = None
    priv_key: Optional[bytes] = None
    activate: int = 0
    voted: int = 0

class User():
    def __init__(self, name: str, dni: str, birth: date, province: str, genre: str, number_tel: int, pub_key: Optional[bytes], 
                priv_key: Optional[bytes], activate: int = 0, voted: int = 0):
        self.name = name
        self.dni = dni
        self.birth = birth
        self.province = province
        self.genre =  genre
        self.number_tel = number_tel
        self.pub_key = pub_key
        self.priv_key = priv_key
        self.activate = activate
        self.voted = voted

    def get_user(self):
        return f"User(name={self.name}, dni={self.dni}, birth={self.birth}, province={self.province}, genre={self.genre}, number_tel={self.number_tel}, pub_key={self.pub_key}, priv_key={self.priv_key}, activate={self.activate})"
    