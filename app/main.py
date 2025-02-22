from fastapi import FastAPI
from app.routers import patients, staffs

app = FastAPI(title="smt health company")

app.include_router(patients.router)
app.include_router(staffs.router)

@app.get("/")
def read_root():
    return {"message": "Main endpoint"}