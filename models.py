from sqlmodel import Field , SQLModel

class Todos(SQLModel , table = True):
    id : int | None = Field(default = None , primary_key = True , )
    title : str
    description : str
    completion : bool