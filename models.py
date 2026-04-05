from pydantic import BaseModel, Field

class SequenceInput(BaseModel):
    sequence: str = Field(pattern=r"^[ACDEFGHIKLMNPQRSTVWY]+$")