from pydantic import BaseModel, ConfigDict, field_validator

class ApplicationCreate(BaseModel):
    company: str
    position: str
    status: str

    @field_validator("company", "position")
    @classmethod
    def validate_text_fields(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("field cannot be empty")

        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        value= value.strip()
        value= value.lower()
        allowed_statuses= ["applied", "interview", "offer", "selected", "rejected"]
        if not value:
            raise ValueError("status cannot be empty")
        if value not in allowed_statuses:
            raise ValueError("invalid status")
        return value


class ApplicationResponse(BaseModel):
    id : int
    company : str
    position: str
    status  : str

    model_config = ConfigDict(from_attributes = True)

class ApplicationDelete(BaseModel):
    message : str

class ApplicationUpdate(BaseModel):
    company : str | None = None
    position: str | None = None
    status  : str | None = None