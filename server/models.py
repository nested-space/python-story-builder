from pydantic import BaseModel, Field, condecimal
from decimal import Decimal

class GenerateResponse(BaseModel):
    text: str = Field(..., description="A single filled flash‐fiction template")

class GenerateParams(BaseModel):
    silliness: condecimal(ge=Decimal('0.0'), le=Decimal('1.0')) = Field(
        0.0,
        description="Probability of choosing comical over serious for each placeholder"
    )
