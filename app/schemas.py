from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    company : str 
    position: str 
    status  : str 


class ApplicationResponse(BaseModel):
    id : int
    company : str 
    position: str 
    status  : str

    model_config = ConfigDict(from_attributes = True)

class ApplicationDelete(BaseModel):
    message : str

    model_config = ConfigDict(from_attributes = True)