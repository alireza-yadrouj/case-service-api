from pydantic import BaseModel

class Case(BaseModel):
    title: str
    description: str
    priority: int


class CaseResponse(BaseModel):
    id : int
    title: str
    description: str
    priority: int

class CaseListResponse(BaseModel):
    total: int
    items: list[CaseResponse]

class TotalCountResponse(BaseModel):
    total: int



