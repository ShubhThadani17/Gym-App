#all endpoints


from fastapi import APIRouter , Depends , HTTPException , status
from services.member_service import create_member , get_member , get_all_members , update_member , delete_member
from database.db import get_db

router = APIRouter()

@router.post("/members")
def create_member_endpoint(member_data , db=Depends(get_db)):
    return create_member(db , member_data)

@router.get("/members/{member_id}")
def get_member_endpoint(member_id : int , db=Depends(get_db)):
    member = get_member(db , member_id)
    if not member :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member

@router.get("/members")
def get_all_members_endpoint(db=Depends(get_db)):
    return get_all_members(db)

@router.put("/members/{member_id}")
def update_member_endpoint(member_id : int , new_data : dict , db=Depends(get_db)):
    return update_member(db , member_id , new_data)

@router.delete("/members/{member_id}")
def delete_member_endpoint(member_id : int , db=Depends(get_db)):
    return delete_member(db , member_id)