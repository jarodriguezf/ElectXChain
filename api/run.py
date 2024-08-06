import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.register import dni_nie_validation, is_adult
from app.models.user import User,  UserSchema
from app.models.db import StructTableDbUsers, InsertDataDbUsers, ShowDniExists, ShowTelephoneExists

app = FastAPI()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


# **CREATE TABLE DB (DONT EXECUTE IF YOU HAVE A TABLE, THE EXECUTE DROP THE TABLE AND CREATE IT AGAIN)**
#create_db = StructTableDbUsers()
#create_db.create_table()


# REGISTER PAGE
@app.get("/", response_class = HTMLResponse)
async def register_index(request: Request):
     try:
          return templates.TemplateResponse("index.html", {"request": request})
     except TypeError as e:
          logger.error(f'Error: {e}')
          raise HTTPException(status_code=500, detail="Internal Server Error")
     except Exception as e:
          logger.error(f'Unexpected error: {e}')
          raise HTTPException(status_code=500, detail='Internal Server Error')


# SEND USERS DATA TO DB
@app.post("/register")
async def save_data_user(user: UserSchema):
     try:
          # CLASSES
          insertNewData = InsertDataDbUsers()
          NIEexists = ShowDniExists()
          TelExists = ShowTelephoneExists()

          user_instance = User(**user.dict())
          logger.debug(f"Received user instance: {user_instance.get_user()}")

          # VALIDATION FIELDS
          if not dni_nie_validation(user_instance.dni):
               logger.error('Error: DNI incorrect')
               raise HTTPException(status_code=400, detail="Incorrect DNI format")
          
          if not is_adult(user_instance.birth):
               logger.error('Error: you need to be 18 years or older')
               raise HTTPException(status_code=400, detail="User must be 18 years or older")
          
          if NIEexists.show_dni_exists(user_instance.dni):
               logger.error('Error: DNI already exists for a user')
               raise HTTPException(status_code=400, detail="User exists for that DNI")
          
          if TelExists.show_telephone_exists(user_instance.number_tel):
               logger.error('Error: Telephone already exists for a user')
               raise HTTPException(status_code=400, detail="User exists for that Telephone")
          # SAVE THE USER
          insertNewData.insert_data_db(user_instance=user_instance)
          return {"message": "User data received"}
     
     except ValidationError as e:
        logger.error(f'ValidationError: {e}')
        raise HTTPException(status_code=422, detail="Validation error")
     except ValueError as e:
          logger.error(f'ValueError: {e}')
          raise HTTPException(status_code=400, detail=str(e))
     except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    