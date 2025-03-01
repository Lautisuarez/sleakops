from fastapi import APIRouter, Depends
from sqlmodel import Session

from services.load_data_service import LoadDataService
from db import get_session


router = APIRouter(prefix="/load_data")

@router.post('/' ,response_model=str)
def load_data(db: Session = Depends(get_session)):
    """
        This endpoint loads data from the URL to the database. \n
        URL: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/index.json \n
        It may takes a few minutes.
    """
    service = LoadDataService(db)
    service.load_data()
    return "The JSON data was successfully loaded into the database."