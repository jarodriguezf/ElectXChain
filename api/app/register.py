from datetime import datetime, date


# VALIDATE THE NIE 
def nie_validation(nie: str) -> bool:
    table = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
    numbers = "1234567890"
    nie = nie.upper()
    if len(nie) == 9:
        dig_control = nie[8]
        nie = nie[:8]
        if nie[0] in dig_ext:
            nie = nie.replace(nie[0], reemp_dig_ext[nie[0]])
        return len(nie) == len([n for n in nie if n in numbers]) \
            and table[int(nie)%23] == dig_control
    return False


# CHECK IF THE USER IS AN ADULT OR NOT
def is_adult(birthdate: date) -> bool:
    today = datetime.today().date()  
    age = today.year - birthdate.year 
    
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    
    return age >= 18


