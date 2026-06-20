
from fastapi import APIRouter , Depends 
from database.db import get_db
from core.auth import get_current_user
from database.models import User
from services.dashboard_service import get_dashboard_stats
from database.schemas import DashboardResponse

router=APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(db = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_dashboard_stats(db,current_user.id)