from pydantic import BaseModel, Field
from typing import List, Optional

class Gate(BaseModel):
    requirement: str
    type: str = "automated"

class Principle(BaseModel):
    principle_id: str
    title: str
    description: str
    checkpoints_or_gates: List[Gate]

class Category(BaseModel):
    title: str
    weight: float = 1.0
    principles: List[Principle]

class FrameworkRoot(BaseModel):
    governing_functions: List[Category]
