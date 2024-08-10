from pydantic import BaseModel
from typing import Optional

class TokenSchema(BaseModel):
    number_tel: Optional[int] = None
    id: Optional[str] = None

class TokenInputSchema(BaseModel):
    token: str