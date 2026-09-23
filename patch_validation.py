from pydantic import BaseModel
from typing import Optional

class patch_input_validate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    completed : Optional[bool] = None
