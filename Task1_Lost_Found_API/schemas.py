from pydantic import BaseModel, field_validator
from typing import Optional


class Item(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title must not be empty")

        return value


class ItemCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title must not be empty")

        return value


class ItemUpdate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title must not be empty")

        return value