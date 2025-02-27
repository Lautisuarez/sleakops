from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from services.load_data_service import LoadDataService
from db import get_session


router = APIRouter(prefix="/load_data")

@router.post('/' ,response_model=str)
def load_data(db: Session = Depends(get_session)):
    try:
        service = LoadDataService(db)
        service.load_data()
        db.commit()
        return "The JSON data was successfully loaded into the database."
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))