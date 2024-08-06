from datetime import datetime, date
import re

# VALIDATE THE NIE 
def dni_nie_validation(dni: str) -> bool:
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
            and tabla[int(dni)%23] == dig_control
    return False


# CHECK IF THE USER IS AN ADULT OR NOT
def is_adult(birthdate: date) -> bool:
    today = datetime.today().date()  
    age = today.year - birthdate.year 
    
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    
    return age >= 18


