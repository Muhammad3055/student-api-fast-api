# student-api-fast-api
# 🎓 Student Management API (FastAPI)

A simple **Student Management REST API** built with [FastAPI](https://fastapi.tiangolo.com/).  
This API allows you to **add, view, update, and delete students**.  
Data is stored in memory (Python list) for simplicity — no database required.

---

## Features
- Get all students
- Get a student by ID
- Add a new student
- Update an existing student
- Delete a student
- Data validation with **Pydantic**

---

##  Tech Stack
- [Python 3.8+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)

---

## 📦 Installation
## install virtual setup
python -m venv .venv
## for activate
.venv\Scripts\activate
## then for fast-api setup
pip install fastapi uvicorn
## for pydantic
pip install pydantic
## make main.py and paste the code there 
main.py
## Run api
uvicorn main:app --reload
## after paste your request url in postman to verify and use Get,Post,Put,delete api functions
## install or run in postman
https://www.postman.com/



