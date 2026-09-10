from pydantic import BaseModel
from typing import Optional
from validate import ValidInputs

class patch_input_validate(BaseModel):
    title : Optional[str]
    description : Optional[str]
    completed : Optional[bool]
