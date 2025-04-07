from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    description: str | None = None

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    id: int

    class Config:
        orm_mode = True
