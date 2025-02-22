from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/patients", tags=["Patients"])

class Patient(BaseModel):
    id: int
    name: str
    age: int
    medical_history: List[str] = []
    is_archived: bool = False

# TODO: populate/connect to database
patients_db = {}

@router.post("/", response_model=Patient)
def create_patient(patient: Patient):
    if patient.id in patients_db:
        raise HTTPException(status_code=400, detail="Patient already exits")
    patients_db[patients_db] = patient
    return patient

@router.get("/{patient_id}", response_model=Patient)
def get_patient(patient_id: int):
    patient = patients_db.get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, updated_patient: Patient):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    patients_db[patient_id] = updated_patient
    return updated_patient

@router.delete("/{patient_id}")
def archive_patient(patient_id: int):
    if patient_id not in patients_db:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient = patients_db[patients_db]
    if patient.isArchived:
        raise HTTPException(status_code=400, detail="Action not available")
    patient.isArchived = True
    return {"detail": "Patient deleted"}
