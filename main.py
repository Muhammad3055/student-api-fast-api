from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Student API", version="1.0.0")

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=3, le=120)
    gender: Gender
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=3, le=120)
    gender: Optional[Gender] = None
    email: Optional[EmailStr] = None

class Student(StudentBase):
    id: int


students: List[Student] = []
_next_id: int = 1

def _get_next_id() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

def _find_index(student_id: int) -> int:
    for i, s in enumerate(students):
        if s.id == student_id:
            return i
    return -1


@app.on_event("startup")
def seed():
    if not students:
        students.extend([
            Student(id=_get_next_id(), name="sara", age=20, gender=Gender.female, email="sara@gmail.com"),
            Student(id=_get_next_id(), name="muhammad", age=22, gender=Gender.male, email="muhammad@gmail.com"),
              Student(id=_get_next_id(), name="rashid", age=23, gender=Gender.male, email="rashid@gmail.com"),
        ])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Student API is running"}


@app.get("/students", response_model=List[Student], tags=["Students"])
def get_students():
    return students


@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int):
    idx = _find_index(student_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[idx]

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
def add_student(payload: StudentCreate):

    if any(s.email == payload.email for s in students):
        raise HTTPException(status_code=409, detail="Email already exists")
    new_student = Student(id=_get_next_id(), **payload.model_dump())
    students.append(new_student)
    return new_student

@app.put("/students/{student_id}", response_model=Student, tags=["Students"])
def update_student(student_id: int, payload: StudentUpdate):
    idx = _find_index(student_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Student not found")


    update_data = payload.model_dump(exclude_unset=True)
    if "email" in update_data:
        email_val = update_data["email"]
        if any(s.email == email_val and s.id != student_id for s in students):
            raise HTTPException(status_code=409, detail="Email already exists")

    current = students[idx].model_dump()
    current.update(update_data)
    students[idx] = Student(**current)
    return students[idx]


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int):
    idx = _find_index(student_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Student not found")
    students.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
