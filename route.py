from fastapi import APIRouter, HTTPException, Query, Path
from model import StudentCreate, StudentUpdate, StudentResponse
from db import students_collection
from bson import ObjectId

router = APIRouter()

def transform_student(student):
    student["_id"] = str(student["_id"])
    return student

@router.get("/", status_code=200)
async def create_student():
    return {"message": "success"}

# 1. Create Student
@router.post("/students", status_code=201)
async def create_student(student: StudentCreate):
    result = students_collection.insert_one(student.dict())
    return {"id": str(result.inserted_id)}

# 2. List Students
@router.get("/students")
async def list_students(country: str = Query(None), age: int = Query(None)):
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}
    students = students_collection.find(query)
    return {"data": [transform_student(s) for s in students]}

# 3. Fetch Student by ID
@router.get("/students/{id}", response_model=StudentResponse)
async def fetch_student(id: str = Path(...)):
    student = students_collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return transform_student(student)

# 4. Update Student
@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: StudentUpdate):
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    result = students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return

# 5. Delete Student
@router.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    result = students_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
