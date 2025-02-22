from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict

router = APIRouter(prefix="/staff", tags=["Staffs"])

class Staff(BaseModel):
    id: int
    name: str
    role: str
    permissions: Optional[List[str]] = []
    is_archived: bool = False

staff_db:Dict[int, Staff] = {}

def admin_required(x_staff_role: str = Header(...)):
    if x_staff_role.lower() != "admin":
        raise HTTPException(
            status_code=403, detail= "Admin privileges required"
        )
    return x_staff_role

@router.post("/", response_model=Staff)
def create_staff(staff: Staff, current_role: str = Depends(admin_required)):
    if staff.id in staff_db:
        raise HTTPException(status_code=400, detail="already exists")
    staff_db[staff.id] = staff
    return staff


@router.get("/{staff_id}", response_model=Staff)
def get_staff(staff_id: int):
    staff_member = staff_db.get(staff_id)
    if not staff_member:
        raise HTTPException(status_code=404, detail="Not found")
    return staff_member

@router.put("/{staff_id}", response_model=Staff)
def update_staff(staff_id: int, updated_staff: Staff, current_role: str = Depends(admin_required)):
    if staff_id not in staff_db:
        raise HTTPException(status_code=404, detail="Not found")
    staff_db[staff_id] = update_staff
    return update_staff

@router.delete("/{staff_id}")
def archive_staff(staff_id: int, current_role: str = Depends(admin_required)):
    if staff_id not in staff_db:
        raise HTTPException(status_code=404, detail="Not found")
    staff_member = staff_db[staff_id]
    if staff_member.isArchived: 
        raise HTTPException(status_code=400, detail="Action not available")
    staff_db[staff_id] = staff_member
