from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# MongoDB Connection
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["school"]
students_collection = db["students"]

# Pydantic Model for Student
class Student(BaseModel):
    name: str
    roll: int
    reg: int
    address: str
    department: str

# Helper function to format MongoDB data
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "roll": student["roll"],
        "reg": student["reg"],
        "address": student["address"],
        "department": student["department"],
    }

# Create Student (POST)
@app.post("/students/")
async def create_student(student: Student):
    student_dict = student.dict()
    result = await students_collection.insert_one(student_dict)
    created_student = await students_collection.find_one({"_id": result.inserted_id})
    return student_helper(created_student)

# Get All Students (GET)
@app.get("/students/")
async def get_students():
    students = await students_collection.find().to_list(1000)
    return [student_helper(student) for student in students]

# Get Single Student by ID (GET)
@app.get("/students/{student_id}")
async def get_student(student_id: str):
    student = await students_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return student_helper(student)
    raise HTTPException(status_code=404, detail="Student not found")

# Update Student (PUT)
@app.put("/students/{student_id}")
async def update_student(student_id: str, student: Student):
    student_dict = student.dict()
    result = await students_collection.update_one({"_id": ObjectId(student_id)}, {"$set": student_dict})
    if result.modified_count:
        updated_student = await students_collection.find_one({"_id": ObjectId(student_id)})
        return student_helper(updated_student)
    raise HTTPException(status_code=404, detail="Student not found")

# Delete Student (DELETE)
@app.delete("/students/{student_id}")
async def delete_student(student_id: str):
    result = await students_collection.delete_one({"_id": ObjectId(student_id)})
    if result.deleted_count:
        return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")

# Run the server
# uvicorn main:app --reload
