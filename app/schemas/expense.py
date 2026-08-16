from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)

    @field_validator("title", "category")
    @classmethod
    def strip_whitespace(cls, value:str) ->str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty")

        return value

class ExpenseUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)

    @field_validator("title", "category")
    @classmethod
    def strip_whitespace(cls, value:str) ->str:
            value = value.strip()
    
            if not value:
                raise ValueError("Value cannot be empty")
    
            return value
class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)