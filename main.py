from fastapi import FastAPI
from routers import students

app = FastAPI(title= "API CON ROUTER DE ESTUDIANTES")

app.include_router(students.router)