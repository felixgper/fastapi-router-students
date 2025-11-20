from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix= "/students", tags= ["students"], responses= {404: {"message" : "No encontrado"}})

class Students(BaseModel):
    id: int
    name: str
    age: int
    active: bool
    
list_students = []

@router.get("/", response_model=list[Students])
async def get_stundets():
    if not list_students:
        return "LA LISTA DE ESTUDIANTES ESTÁ VACÍA"
    return list_students

@router.get("/{id}", response_model=Students)
async def get_students(id: int):
    existing = search_id(id)
    if existing is None:
        raise HTTPException(status_code= 404, detail= "ESTUDIANTE NO ENCONTRADO")
    return existing

@router.post("/")
async def post_students(student : Students):
    existing_student = search_id(student.id)
    if existing_student is not None:
        raise HTTPException(status_code= 409, detail= "EL ID YA EXISTE")
    list_students.append(student)
    return student

@router.put("/{id}")
async def put_students(id:int, student : Students):
    
    found = False
    
    for index, value in enumerate(list_students):
        if value.id == id:
            list_students[index] = student
            found = True
            return {"message" : "Estudiante Actualizado", "Actualizado" : student}
    
    if not found:
        raise HTTPException(status_code= 404, detail= "ID NO ENCONTRADO")
    
@router.delete("/{id}")
async def deleted_students(id:int):
    
    found = False
    
    for index, value in enumerate(list_students):
        if value.id == id:
            del list_students[index]
            found = True
            return {"message" : "Estudiante Eliminado"}
    
    if not found:
        raise HTTPException(status_code= 404, detail= "ID NO ENCONTRADO")


def search_id(id: int):
    for student in list_students:
        if student.id == id:
            return student
    return None