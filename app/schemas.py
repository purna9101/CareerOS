from pydantic import BaseModel, ConfigDict, field_validator, BeforeValidator
from enum import Enum
from typing import Annotated


class ApplicationStatus(Enum):
    APPLIED=   "applied"
    INTERVIEW= "interview"
    OFFER=     "offer"
    SELECTED=  "selected"
    REJECTED=  "rejected"

def normalize_status(value):
    value= value.strip()
    value= value.lower()
    if not value:
        raise ValueError("Invalid Status ")
        
    return value

def normalize_text(value):
    value= value.strip()
    if not value:
        raise ValueError("field cannot be empty")

    return value

Status = Annotated[
    ApplicationStatus,
    BeforeValidator(normalize_status)
]

NonEmptyString= Annotated[
    str,
    BeforeValidator(normalize_text)
]


class ApplicationCreate(BaseModel):
    company: NonEmptyString
    position: NonEmptyString
    status: Status


class ApplicationResponse(BaseModel):
    id : int
    company : str
    position: str
    status  : str

    model_config = ConfigDict(from_attributes = True)

class ApplicationDelete(BaseModel):
    message : str

class ApplicationUpdate(BaseModel):
    company : NonEmptyString | None = None
    position: NonEmptyString | None = None
    status  : Status | None = None