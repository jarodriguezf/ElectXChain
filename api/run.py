from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models import User, StructTableDbUsers

app = FastAPI()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

create_db = StructTableDbUsers()
create_db.create_table()

# REGISTER PAGE
@app.get("/", response_class = HTMLResponse)
async def register_index(request: Request):
     return templates.TemplateResponse("index.html", {"request": request})


# SEND USERS DATA IN DBB
@app.post("/register")
async def save_data_user(user: User):
     print(user)


if __name__ == "__main__":
     register_index()