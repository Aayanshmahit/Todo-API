from sqlmodel import Field , SQLModel , create_engine

engine = create_engine("sqlite:///todos.db")

class Todos(SQLModel , table = True):
    id : int | None = Field(default = None , primary_key = True , )
    title : str
    description : str
    completion : bool

SQLModel.metadata.create_all(engine)