from pydantic import BaseModel
from typing import Optional

class ValidInputs(BaseModel):
    id : int
    title : str
    description : str
    completed : Optional[bool] = False

