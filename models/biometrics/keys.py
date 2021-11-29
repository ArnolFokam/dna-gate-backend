from typing import Optional, List

from pydantic import BaseModel


class ApiKey(BaseModel):
    api_key: str
    scopes: Optional[List[str]]
