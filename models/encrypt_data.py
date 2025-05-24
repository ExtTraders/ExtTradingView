from pydantic import BaseModel

class EncryptData(BaseModel):
    access_key: str
    secret_key: str