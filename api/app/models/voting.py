from pydantic import BaseModel

#USER STRUCTURE (2FA)
class VoteSchema(BaseModel):
    id: str
    vote: str