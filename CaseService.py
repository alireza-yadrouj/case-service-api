from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

project = FastAPI()

cases = []

case_id_counter = 1

class Case(BaseModel):
    title: str
    description: str
    priority: int

class CaseOut(BaseModel):
    id: int
    title: str
    description: str
    priority: int


@project.post("/cases")
def create_case(case: Case):
    global case_id_counter

    new_case={
        "id": case_id_counter,
        "title": case.title,
        "description": case.description,
        "priority":case.priority

    }

    cases.append(new_case)
    case_id_counter += 1

    return new_case


@project.get("/cases", response_model=list[CaseOut])
def get_cases():
    return cases

@project.put("/cases/{case_id}", response_model=CaseOut)
def update_case(case_id: int, updated_case: Case):
    for case in cases:
        if case["id"] == case_id:
            case["title"] = updated_case.title
            case["description"] = updated_case.description
            case["priority"] = updated_case.priority
            return case

    raise HTTPException(status_code=404, detail="Case not found")

@project.delete("/cases/{case_id}")
def delete_case(case_id: int):
    for index, case in enumerate(cases):
        if case["id"] == case_id:
            cases.pop(index)
            return {"message": "Case deleted"}

    raise HTTPException(status_code=404, detail="Case not found")


@project.get("/")
def say_hello():
    return {"message": "Hello app!!!!"}
