import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.models.user import User,  UserSchema
from app.models.db import StructTableDbUsers, InsertDataDbUsers

app = FastAPI()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


# **CREATE TABLE DB (DONT EXECUTE IF YOU HAVE A TABLE, THE EXECUTE DROP THE TABLE AND CREATE IT AGAIN)**
# create_db = StructTableDbUsers()
# create_db.create_table()


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
          insertNewData = InsertDataDbUsers()

          user_instance = User(**user.dict())
          logger.debug(f"Received user instance: {user_instance.get_user()}")

          insertNewData.insert_data_db(user_instance=user_instance)
          return {"message": "User data received"}
     except ValidationError as e:
        logger.error(f'ValidationError: {e}')
        raise HTTPException(status_code=422, detail="Validation error")
     except ValueError as e:
          logger.error(f'ValueError: {e}')
          raise HTTPException(status_code=400, detail="Invalid user data")
     except Exception as e:
        logger.error(f'Unexpected error: {e}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
    