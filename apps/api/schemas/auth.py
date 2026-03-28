
from pydantic import BaseModel


class MicrosoftLoginRequest(BaseModel):
    id_token: str
