from math import degrees
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ContactModel(BaseModel):
    email: EmailStr = Field(...)
    linkedin: str = Field(...)
    github: str = Field(...)
    phone: str = Field(...)
    
class ExperienceModel(BaseModel):
    start_date: str = Field(...)
    end_date: str = Field(...)
    skills: list = Field(...)

class EducationModel(BaseModel):
    start_date: str = Field(...)
    end_date: str = Field(...)
    degrees: list = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class StudentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    contact: ContactModel = Field(...)
    skills: list = Field(...)
    degrees: list = Field(...)
    majors: list = Field(...)
    experiences:list=Field(...)
    education:list=Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
