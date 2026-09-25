from sqlmodel import Field , SQLModel

class Todos(SQLModel , table = True):
    id : int | None = Field(default = None , primary_key = True , )
    title : str
    desription : str
    completion : bool