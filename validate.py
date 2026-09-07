from pydantic import BaseModel
from typing import Optional

class ValidInputs(BaseModel):
    title : str
    description : str
    completed : Optional[bool] = False

