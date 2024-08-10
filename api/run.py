import logging
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.register import dni_nie_validation, is_adult
from app.models.user import User,  UserSchema, UserAutSchema, PhoneNumberSchema
from app.models.db import ShowsDataDbUsers, InsertDataDbUsers, StructTableDbUsers
from app.models.two_factor import TokenSchema
from app.autentication import get_token, validate_token
import asyncio
import time

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
          showsData = ShowsDataDbUsers()

          user_instance = User(**user.dict())
          logger.debug(f"Received user instance: {user_instance.get_user()}")

          # VALIDATION FIELDS
          if not dni_nie_validation(user_instance.dni):
               logger.error('Error: DNI incorrect')
               raise HTTPException(status_code=400, detail="Incorrect DNI format")
          
          if not is_adult(user_instance.birth):
               logger.error('Error: you need to be 18 years or older')
               raise HTTPException(status_code=400, detail="User must be 18 years or older")
          
          if showsData.show_dni_exists(user_instance.dni):
               logger.error('Error: DNI already exists for a user')
               raise HTTPException(status_code=400, detail="User exists for that DNI")
          
          if showsData.show_telephone_exists(user_instance.number_tel):
               logger.error('Error: Telephone already exists for a user')
               raise HTTPException(status_code=400, detail="User exists for that Telephone")
          
          # SAVE THE USER
          insertNewData.insert_data_db(user_instance=user_instance)
          return {"message": "User data received"}
     except HTTPException as e:
          logger.error(f'HTTPException: {e.detail}')
          raise e
     except ValueError as e:
          logger.error(f'ValueError: {e}')
          raise HTTPException(status_code=400, detail=str(e))
     except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
     

# AUTENTICATION PAGE
@app.get("/page_autentication", response_class = HTMLResponse)
async def autenticate_page(request: Request):
     try:
          return templates.TemplateResponse("autentication.html", {"request": request})
     except TypeError as e:
          logger.error(f'Error: {e}')
          raise HTTPException(status_code=500, detail="Internal Server Error")
     except Exception as e:
          logger.error(f'Unexpected error: {e}')
          raise HTTPException(status_code=500, detail='Internal Server Error')
     

# SEND DNI/NIE AND TELEPHONE NUMBER TO VALIDATE THE REGISTERED USER
@app.post("/autentication")
async def validate_data_register_user(user: UserAutSchema):
     try:
          dni = user.dni
          number_tel = user.number_tel
          showsData = ShowsDataDbUsers()

          # VALIDATION IN THE SYSTEM
          if not showsData.show_dni_tel_exists_for_a_user(dni, number_tel):
               logger.error(f'Error: The user not exists, try to register first')
               raise HTTPException(status_code=400, detail="User not exists in the system")
          
          # start coroutines
          asyncio.create_task(simulate_sms(PhoneNumberSchema(number_tel=number_tel)))

          redirect_url = f"/2fa_validation?number_tel={number_tel}"
          return RedirectResponse(url=redirect_url, status_code = 302)
     except HTTPException as e:
          logger.error(f'HTTPException: {e.detail}')
          raise e
     except Exception as e:
          logger.error(f'Unexpected error: {e}')
          raise HTTPException(status_code=500, detail='Internal Server Error')
     

# RETURN TOKEN (SIMULATION SMS)
@app.post('/recive_sms')
async def simulate_sms(data_number: PhoneNumberSchema):
     try:
          number_tel = data_number.number_tel
          token = get_token()

          logger.info(f"Simulating the sending of SMS to {number_tel}...")

          await asyncio.sleep(10)

          logger.info(f"📲 Simulating SMS Reception")
          logger.info(f"📞 Number: {number_tel}")
          logger.info(f"🔑 Code: {token}")
          logger.info(f"✅ SMS successfully simulated at {number_tel}.")

          return {"status": "token_generated"}
     except Exception as e:
          logger.error(f'Error: The system failed in the processing of the sms - {str(e)}')
          return HTTPException(status_code=500, detail='Internal Server Error')


# 2FA PAGE
@app.get("/2fa_validation", response_class=HTMLResponse)
async def two_factor_page(request: Request, number_tel: int = Query(...)):
    try:
        return templates.TemplateResponse("twofactor.html", {"request": request, "number_tel": number_tel})
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
     

# VALIDATE THE TOKEN INPUT
@app.post("/validation_token_2fa")
async def validate_data_register_user(input: TokenSchema):
     try:
          input_token = input.token
          
          if not validate_token(input_token):
               raise HTTPException(status_code=400, detail='Error: Invalid token')

          return {'message': 'Valid token'}
     except HTTPException as e:
          logger.error(f'HTTPException: {e.detail}')
          raise e
     except Exception as e:
          logger.error(f'Unexpected error: {e}')
          raise HTTPException(status_code=500, detail='Internal Server Error')