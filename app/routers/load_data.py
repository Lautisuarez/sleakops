from fastapi import APIRouter, Depends
from sqlmodel import Session

from services.load_data_service import LoadDataService
from db import get_session


router = APIRouter(prefix="/load_data")

@router.post('/' ,response_model=str)
def load_data(db: Session = Depends(get_session)):
    service = LoadDataService(db)
    service.load_data()
    return "The JSON data was successfully loaded into the database."