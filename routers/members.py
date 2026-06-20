#all endpoints


from fastapi import APIRouter , Depends , HTTPException , status , Query
from services.member_service import create_member , get_member , get_all_members , update_member , delete_member , search_member
from database.db import get_db
from core.auth import get_current_user
from database.models import User
from database.schemas import MemberCreate , MemberUpdate , MemberResponse
from typing import List

router = APIRouter()

@router.post("/members", response_model=MemberResponse)
def create_member_endpoint(member_data : MemberCreate , db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_member(db , member_data,current_user.id)

@router.get("/members/{member_id}", response_model=MemberResponse)
def get_member_endpoint(member_id : int , db=Depends(get_db), current_user: User = Depends(get_current_user)):
    member = get_member(db , member_id,current_user.id)
    if not member :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member

@router.get("/members/search", response_model=List[MemberResponse])
def search_member_endpoint(name: str = Query(min_length=2, max_length=10),db=Depends(get_db),current_user: User = Depends(get_current_user)):
     return search_member(db,current_user.id,name)

@router.get("/members", response_model=List[MemberResponse])
def get_all_members_endpoint(db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_members(db,current_user.id)

@router.put("/members/{member_id}", response_model=MemberResponse)
def update_member_endpoint(member_id : int , new_data : MemberUpdate , db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_member(db , member_id , new_data.model_dump(exclude_unset=True) , current_user.id)

@router.delete("/members/{member_id}")
def delete_member_endpoint(member_id : int , db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_member(db , member_id,current_user.id)