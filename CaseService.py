from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from database import get_connection

project = FastAPI()

cases = []

router = APIRouter()

case_id_counter = 1

class Case(BaseModel):
    title: str
    description: str
    priority: int


class CaseResponse(BaseModel):
    id : int
    title: str
    description: str
    priority: int


@router.post("/cases", response_model=CaseResponse)
def create_case(case: Case):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO cases (title, description, priority) VALUES (?, ?, ?)",
        (case.title, case.description, case.priority)
    )
    conn.commit()

    case_id = cursor.lastrowid
    conn.close()

    return {
        "id": case_id,
        "title": case.title,
        "description": case.description,
        "priority": case.priority
    }

@router.get("/cases", response_model=list[CaseResponse])
def get_cases(priority: int | None = None):
    conn = get_connection()
    cursor = conn.cursor()
    if priority is None:
        rows = cursor.execute( "SELECT * FROM cases" ).fetchall()
    else:
        rows = cursor.execute( "SELECT * FROM cases WHERE priority = ?", (priority,) ).fetchall()

    conn.close()

    return [dict(row) for row in rows]

@router.put("/cases/{case_id}", response_model=CaseResponse)
def update_case(case_id: int, updated_case: Case):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE cases
        SET title = ?, description = ?, priority = ?
        WHERE id = ?
        """,
        (
            updated_case.title,
            updated_case.description,
            updated_case.priority,
            case_id
        )
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Case not found")

    conn.commit()
    conn.close()

    return {
        "id": case_id,
        "title": updated_case.title,
        "description": updated_case.description,
        "priority": updated_case.priority
    }


@router.delete("/cases/{case_id}")
def delete_case(case_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cases WHERE id = ?",
        (case_id,)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Case not found")

    conn.commit()
    conn.close()

    return {"message": "Case deleted"}

@router.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(case_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
     raise HTTPException(status_code=404, detail="Case not found")

    return dict(row)


@project.get("/")
def say_hello():
    return {"message": "Hello app!!!!"}
